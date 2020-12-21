'''A3. Tester for the function common_words in tweets.
'''

import unittest
import tweets

class TestCommonWords(unittest.TestCase):
    '''Tester for the function common_words in tweets.
    '''

    def test_empty(self):
        '''Empty dictionary.'''
        arg1 = {}
        arg2 = 1
        exp_arg1 = {}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be\n {}, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)
    
    def test_no_words_no_limit(self):
        ''' empty dictionary along with at most 0 words '''
        arg1 = {}
        arg2 = 0
        exp_arg1 = {}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None
        
        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be\n {}, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)
        
    def test_tie_of_all_words_one_limit(self):
        '''all words in the dictionary are mentioned the same amount
        of times'''
        arg1 = {'a': 3, 'b': 3}
        arg2 = 1
        exp_arg1 = {}
        act_return = tweets.common_words(arg1, arg2)
        print(arg1)
        exp_return = None
        
        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be\n {}, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)
        
    def test_two_words_one_limit(self):
        '''dictionary with two words, and one limit'''
        arg1 = {'a': 4, 'b': 3}
        arg2 = 1
        exp_arg1 = {'a': 4}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None
        
        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be\n {}, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)             
        
    def test_one_word_limit_one(self):
        '''Dictionary with one word.'''

        arg1 = {'hello': 2}
        arg2 = 1
        exp_arg1 = {'hello': 2}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None
        
        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be\n {}, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)         
      
    def test_less_words_more_limits_unsorted(self):
        '''more limits than words in the dictionary'''
        arg1 = {'a': 2, 'b': 3, 'c': 5}
        arg2 = 4
        exp_arg1 = {'c': 5, 'b': 3, 'a': 2}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None
        
        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be\n {}, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)
             
        
if __name__ == '__main__':
    unittest.main(exit=False)
