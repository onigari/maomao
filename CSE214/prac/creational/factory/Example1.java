public class Example1 {
    public static void main(String[] args) {
        Application app = new PDFApplication();
        app.newDocument();
    }
}

interface Document {
    void open();
}

class PDFDocument implements Document {
    @Override
    public void open() {
        System.out.println("Opening PDF");
    }
}

class DOCXDocument implements Document {
    @Override
    public void open() {
        System.out.println("Opening DOCX");
    }
    
}

abstract class Application {
    public abstract Document createDocument();

    public void newDocument() {
        Document doc = createDocument();
        doc.open();
    }
}

class PDFApplication extends Application {

    @Override
    public Document createDocument() {
        return new PDFDocument();
    }
    
}

class DOCXApplication extends Application {

    @Override
    public Document createDocument() {
        return new DOCXDocument();
    }
    
}