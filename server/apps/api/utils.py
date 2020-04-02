import boto3
import cv2.cv2 as cv2
from django.conf import settings
import json
import numpy as np
import os
import sagemaker
from sagemaker.predictor import RealTimePredictor
import time

from .choices import LOWER_CATEGORY_CHOICES

def byte_to_image(inp):
    """
    converts bytes string to image
    """
    nparr = np.fromstring(inp, np.uint8)
    img = cv2.imdecode(nparr, 1)
    
    return img


def remove_background(image):
    """
    Removes background from image
    """
    # Paramters.
    BLUR = 21
    CANNY_THRESH_1 = 10
    CANNY_THRESH_2 = 200
    MASK_DILATE_ITER = 10
    MASK_ERODE_ITER = 10
    MASK_COLOR = (0.0,0.0,1.0)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Edge detection.
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)
    
    # Find contours in edges, sort by area
    contour_info = []
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]
    
    # Create empty mask.
    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))
    
    # Smooth mask and blur it.
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask]*3)
    
    # Blend masked img into MASK_COLOR background
    mask_stack = mask_stack.astype('float32') / 255.0
    image = image.astype('float32') / 255.0

    masked = (mask_stack * image) + ((1-mask_stack) * MASK_COLOR)
    masked = (masked * 255).astype('uint8')
    
    c_red, c_green, c_blue = cv2.split(image)
    img_a = cv2.merge((c_red, c_green, c_blue, mask.astype('float32') / 255.0))

    return img_a*255
    
    
def image_to_tensor(image):
    """
    receives image and converts it to tensor
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224,224), interpolation=cv2.INTER_AREA)
    image = np.asarray(image)
    image = cv2.normalize(image.astype('float'), None, 0, 1, cv2.NORM_MINMAX)
    image = np.expand_dims(image, axis=0)
    
    return image


def execute_inference(image):
    """
    Receives image and executes 
    inference against sagemaker endpoint.
    """
    
    boto_session = boto3.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    sess = sagemaker.Session(boto_session=boto_session)
    
    ENDPOINT_MODEL = 'clothes-30-model'

    predictor = RealTimePredictor(endpoint=ENDPOINT_MODEL,
                                  sagemaker_session=sess,
                                content_type='application/json',
                                accept='application/json')
    
    # Convert tensor to JSON format.
    image = image.tolist()
    image = json.dumps(image)

    # Get a prediction from the endpoint.
    result = predictor.predict(image)
    # Convert result into python dict.
    result = json.loads(result)

    return result    


def save_image_s3(image):
    """
    Receives image and saves it to s3 bucket,
    returns the url of an uplodaed image.
    """
    TEMP_IMAGE_NAME = 'temp/clothes_' + str(int(round(time.time()*1000))) + '.png'
    BUCKET_NAME = 'otte-bucket'
    REGION_NAME = 'ap-northeast-2'
    
    cv2.imwrite(TEMP_IMAGE_NAME, image)
    
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    
    s3.upload_file(TEMP_IMAGE_NAME, BUCKET_NAME, 'clothes/'+TEMP_IMAGE_NAME, ExtraArgs={'ACL':'public-read'})
    
    url = 'https://' + BUCKET_NAME + '.s3.ap-northeast-2.amazonaws.com/clothes/' + TEMP_IMAGE_NAME

    os.remove(TEMP_IMAGE_NAME)

    return url

def move_image_to_saved(image_url):
    """
    moves image_url from temp to save on s3 bucket
    """
    parts = image_url.split('/')
    
    BUCKET_NAME = parts[2].split('.')[0]
    IMAGE_NAME = parts[-1]
    OBJECT_NAME = 'clothes/temp/' + IMAGE_NAME
    KEY_NAME = 'clothes/saved/' + IMAGE_NAME
    
    COPY_SOURCE = {
        'Bucket': BUCKET_NAME,
        'Key': OBJECT_NAME
    }
    
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    
    # Copy from temp to saved.
    s3.copy_object(Bucket=BUCKET_NAME, 
                   CopySource= COPY_SOURCE, 
                   Key=KEY_NAME,
                   ACL='public-read')
    
    # Delete temp.
    s3.delete_object(Bucket=BUCKET_NAME,
                     Key=OBJECT_NAME)
    
    moved_url = 'https://' + BUCKET_NAME + '.s3.ap-northeast-2.amazonaws.com/' + KEY_NAME
    
    return moved_url

def get_categories_from_predictions(predictions):
    """
    converts prediction result to
    corresponding upper and lower categories
    """
    result = predictions['predictions'][0]
    lower_index = result.index(max(result))
    
    upper = get_upper_category(lower_index)
    lower = LOWER_CATEGORY_CHOICES[lower_index][0]
    
    return (upper, lower)

def get_upper_category(lower_index):
    """
    get upper category of the corresponding
    lower category index
    """
    if lower_index < 11:
        return '상의'
    elif lower_index < 17:
        return '하의'
    elif lower_index < 19:
        return '치마'
    elif lower_index < 33:
        return '아우터'
    else:
        return '원피스'
    
