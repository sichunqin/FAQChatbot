# convert str to the following hyperlink
#<a href="#" onclick="sendLinkText(this);">str</a>
#
def convertToLinkedText(str):
    return r'<a href="#" onclick="sendLinkText(this);">' + str + "</a>"
    pass