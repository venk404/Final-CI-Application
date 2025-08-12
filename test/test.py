import unittest
from unittest.mock import patch, MagicMock
import requests
from dotenv import load_dotenv
import os

load_dotenv()

url = f"{os.getenv('test_url', 'http://localhost')}:{os.getenv('APP_PORT', '8002')}/"


class TestStudentDetailsAPI(unittest.TestCase):
    
    student_id = None
    
    def setUp(self):
        self.url = url
        self.student_data = {
            "name": "Foo",
            "email": "foo@example.com",
            "age": 20,
            "phone": "1234567890"
        }

    @patch('requests.post')
    def test_post_studentdetails(self, mock_post):
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'student_id': {'id': '1'},
            'message': 'Student added successfully'
        }
        mock_post.return_value = mock_response
        
        # Make the request
        response = requests.post(self.url + 'AddStudent', json=self.student_data)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        TestStudentDetailsAPI.student_id = response_data['student_id']['id']
        
        # Verify the mock was called correctly
        mock_post.assert_called_once_with(
            self.url + 'AddStudent',
            json=self.student_data
        )

    @patch('requests.get')
    def test_getALLstudentdetails(self, mock_get):
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'students': [
                {'id': '1', 'name': 'Foo', 'email': 'foo@example.com'},
                {'id': '2', 'name': 'Bar', 'email': 'bar@example.com'}
            ]
        }
        mock_get.return_value = mock_response
        
        # Make the request
        response = requests.get(self.url + 'GetAllStudents')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        
        # Verify the mock was called correctly
        mock_get.assert_called_once_with(self.url + 'GetAllStudents')

    @patch('requests.get')
    def test_GetStudenbyid(self, mock_get):
        # Set up student_id if not available
        if not hasattr(TestStudentDetailsAPI, 'student_id') or TestStudentDetailsAPI.student_id is None:
            TestStudentDetailsAPI.student_id = '1'
        
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': TestStudentDetailsAPI.student_id,
            'name': 'Foo',
            'email': 'foo@example.com',
            'age': 20,
            'phone': '1234567890'
        }
        mock_get.return_value = mock_response
        
        # Make the request
        url_with_id = f"{self.url}GetStudent?id={TestStudentDetailsAPI.student_id}"
        response = requests.get(url_with_id)
        
        # Assertions
        self.assertEqual(response.status_code, 200,
                         f'Expected status code 200 but got {response.status_code}')
        
        # Verify the mock was called correctly
        mock_get.assert_called_once_with(url_with_id)

    @patch('requests.patch')
    def test_Update(self, mock_patch):
        # Set up student_id if not available
        if not hasattr(TestStudentDetailsAPI, 'student_id') or TestStudentDetailsAPI.student_id is None:
            TestStudentDetailsAPI.student_id = '1'
        
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'message': 'Student updated successfully',
            'student_id': TestStudentDetailsAPI.student_id
        }
        mock_patch.return_value = mock_response
        
        # Prepare update data and URL
        url_update = f"{self.url}v2/UpdateStudent?id={TestStudentDetailsAPI.student_id}"
        update_data = {
            'name': 'Ganesh Gaitonde',
            'email': 'Gopalmat@gmail.com',
            'age': 0,
            'phone': '1234567895'
        }
        
        # Make the request
        response = requests.patch(url_update, json=update_data)
        
        # Assertions
        self.assertEqual(response.status_code, 200,
                         f'Expected status code 200 but got {response.status_code}')
        
        # Verify the mock was called correctly
        mock_patch.assert_called_once_with(url_update, json=update_data)

    @patch('requests.delete')
    def test_DeleteStudent(self, mock_delete):
        # Set up student_id if not available
        if not hasattr(TestStudentDetailsAPI, 'student_id') or TestStudentDetailsAPI.student_id is None:
            TestStudentDetailsAPI.student_id = '1'
        
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'message': 'Student deleted successfully',
            'student_id': TestStudentDetailsAPI.student_id
        }
        mock_delete.return_value = mock_response
        
        # Prepare delete URL
        url_delete = f"{self.url}v2/DeleteStudent?id={TestStudentDetailsAPI.student_id}"
        
        # Make the request
        response = requests.delete(url_delete)
        
        # Assertions
        self.assertEqual(response.status_code, 200,
                         f'Expected status code 200 but got {response.status_code}')
        
        # Verify the mock was called correctly
        mock_delete.assert_called_once_with(url_delete)


if __name__ == "__main__":
    # Run tests in order for CI pipeline
    suite = unittest.TestSuite()
    suite.addTest(TestStudentDetailsAPI('test_post_studentdetails'))
    suite.addTest(TestStudentDetailsAPI('test_GetStudenbyid'))
    suite.addTest(TestStudentDetailsAPI('test_getALLstudentdetails'))
    suite.addTest(TestStudentDetailsAPI('test_Update'))
    suite.addTest(TestStudentDetailsAPI('test_DeleteStudent'))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code for CI pipeline
    exit(0 if result.wasSuccessful() else 1)