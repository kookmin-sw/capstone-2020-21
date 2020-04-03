from rest_framework.test import APITestCase

class ClohtesSetCreateTests(APITestCase):
    def setUp(self):
        pass
    
    def test_create(self):
        """
        정상생성 테스트.
        """
        pass
    
    def test_create_required(self):
        """
        필수필드생성 테스트.
        """
        pass
    
    def test_create_error_no_required(self):
        """
        오류 - 필수 필드 없을 경우.
        """
        pass
    
    def test_create_error_authentication(self):
        """
        오류 - 인증정보 오류.
        """
        pass

class ClothesSetRetrieveTests(APITestCase):
    def setUp(self):
        pass
        
    def test_retrieve_one(self):
        """
        단일 코디 정보 반환 테스트.
        """
        pass
        
    def test_retrieve_many(self):
        """
        여러 개 코디 정보 반환 테스트.
        """
        pass
        
    def test_retrieve_me(self):
        """
        내 코디 정보 반환 테스트.
        """
        pass
    
class ClothesSetUpdateTests(APITestCase):
    def setUp(self):
        pass
    
    def test_update_put(self):
        """
        PUT 메소드 테스트.
        """
        pass
    
    def test_update_patch(self):
        """
        PATCH 메소드 테스트.
        """
        pass
    
    def test_update_error_not_mine(self):
        """
        오류 - 해당 사용자의 코디가 아닐 시.
        """
        pass
    
class ClothesSetDeleteTests(APITestCase):
    def setUp(self):
        pass
    
    def test_delete(self):
        """
        정상 삭제 테스트.
        """
        pass
    
    def test_delete_error_not_mine(self):
        """
        오류 - 해당 사용자의 코디가 아닐 시.
        """
        pass
    