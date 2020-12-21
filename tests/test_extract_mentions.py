'''A3. Tester for the function extract_mentions in tweets.
'''

import unittest
import tweets

class TestExtractMentions(unittest.TestCase):
    '''Tester for the function extract_mentions in tweets.
    '''

    def test_empty(self):
        '''Empty tweet.'''

        arg = ''
        actual = tweets.extract_mentions(arg)
        expected = []
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)


    def test_nonempty_no_mention(self):
        '''Non-empty tweet with no mentions.'''

        arg = 'tweet test case'
        actual = tweets.extract_mentions(arg)
        expected = []
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)
        
    def test_one_mention(self):
        '''Non-empty tweet with one mentions.'''

        arg = 'tweet test case @lol!hi'
        actual = tweets.extract_mentions(arg)
        expected = ['lol']
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)
        
    def test_multiple_mentions(self):
        '''Non-empty tweet with multiple mentions.'''

        arg = 'tweet test @##$ @lol!hi @lol @lolol @lolol @hi@lol@lol, @but*&^'
        actual = tweets.extract_mentions(arg)
        expected = ['lol', 'lol', 'lolol', 'lolol', 'hi', 'but']
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)    


if __name__ == '__main__':
    unittest.main(exit=False)
