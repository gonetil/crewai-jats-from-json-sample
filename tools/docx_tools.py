from crewai_tools import DOCXSearchTool

class DocxTools():
    @tool("Analyze paper in docx format, looking for references")
    def look_for_references_in_document(path):
        """Analyses the text of a paper in a docx file, and looks for the reference 
        section. Returns the list of references found in the document
        """
        