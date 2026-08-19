
import java.util.*;

public class Composite1 {

    public static void main(String[] args) {
        Folder root = new Folder("root");
        root.add(new File("readme.txt", 5));
        Folder src = new Folder("src");
        src.add(new File("Main.java", 20));
        src.add(new File("Utils.java", 15));
        root.add(src);

        root.display("");
        System.out.println("Total: " + root.getSize() + " kB");
    }
}

interface FileSystemItem {

    void display(String indent);

    int getSize();
}

class File implements FileSystemItem {

    private String name;
    private int size;

    public File(String name, int size) {
        this.name = name;
        this.size = size;
    }

    @Override
    public void display(String indent) {
        System.out.println(indent + "File: " + name + " (" + size + " kB)");

    }

    public String getName() {
        return name;
    }

    @Override
    public int getSize() {
        return size;
    }

}

class Folder implements FileSystemItem {

    private String name;
    private List<FileSystemItem> children = new ArrayList<>();

    public Folder(String name) {
        this.name = name;
    }

    public void add(FileSystemItem item) {
        children.add(item);
    }

    public void remove(FileSystemItem item) {
        children.remove(item);
    }

    @Override
    public void display(String indent) {
        System.out.println(indent + "Folder: " + name);
        for (FileSystemItem child : children) {
            child.display(indent + " ");
        }
    }

    @Override
    public int getSize() {
        int sz = 0;
        for (FileSystemItem child : children) {
            sz += child.getSize();
        }
        return sz;
    }

}
