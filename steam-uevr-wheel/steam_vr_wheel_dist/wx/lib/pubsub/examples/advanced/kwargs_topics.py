# Automatically generated by TopicTreeSpecPrinter(**kwargs).
# The kwargs were:
# - fileObj: file
# - width: 70
# - treeDoc: None
# - indentStep: 4
# - footer: '# End of topic tree definition. Note that application may l...'


class topic_1:
    """
    Explain when topic_1 should be used
    """

    def msgDataSpec(msg):
        """
        - msg: a text string message for recipient
        """

    class subtopic_11:
        """
        Explain when subtopic_11 should be used
        """

        def msgDataSpec(msg, msg2, extra=None):
            """
            - extra: something optional
            - msg2: a text string message #2 for recipient
            """

class topic_2:
    """
    Some something useful about topic2
    """

    def msgDataSpec(msg=None):
        """
        - msg: a text string
        """

    class subtopic_21:
        """
        description for subtopic 21
        """

        def msgDataSpec(msg, arg1=None):
            """
            - arg1: UNDOCUMENTED
            """


# End of topic tree definition. Note that application may load
# more than one definitions provider.
