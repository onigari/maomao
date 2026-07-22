// Common Interface
interface Report {
    void open();
    void generate();
}

// Concrete Report Types
class PDFReport implements Report {
    public void open() { System.out.println("Opening PDF Report..."); }
    public void generate() { System.out.println("Generating PDF Report..."); }
}

class WordReport implements Report {
    public void open() { System.out.println("Opening Word Report..."); }
    public void generate() { System.out.println("Generating Word Report..."); }
}

class HTMLReport implements Report {
    public void open() { System.out.println("Opening HTML Report..."); }
    public void generate() { System.out.println("Generating HTML Report..."); }
}

abstract class ReportProcessor {
    
    // The Factory Method: Specialized subclasses must implement this 
    // to decide which concrete Report object gets created.
    protected abstract Report createReport();

    // The common processing steps defined in one place
    public void processReport() {
        // 1. Create the report object (Delegated to subclass)
        Report report = createReport();
        
        // 2. Open the report
        report.open();
        
        // 3. Generate the report
        report.generate();
        
        // 4. Display a completion message
        System.out.println("Status: Report processing successfully completed.\n");
    }
}

class PDFProcessor extends ReportProcessor {
    @Override
    protected Report createReport() {
        return new PDFReport();
    }
}

class WordProcessor extends ReportProcessor {
    @Override
    protected Report createReport() {
        return new WordReport();
    }
}

class HTMLProcessor extends ReportProcessor {
    @Override
    protected Report createReport() {
        return new HTMLReport();
    }
}

public class FactoryMethodDemo {
    public static void main(String[] args) {
        
        System.out.println("--- Processing PDF ---");
        ReportProcessor pdfProcessor = new PDFProcessor();
        pdfProcessor.processReport();

        System.out.println("--- Processing Word ---");
        ReportProcessor wordProcessor = new WordProcessor();
        wordProcessor.processReport();
        
        System.out.println("--- Processing HTML ---");
        ReportProcessor htmlProcessor = new HTMLProcessor();
        htmlProcessor.processReport();
    }
}
