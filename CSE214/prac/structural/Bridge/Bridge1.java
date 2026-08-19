
public class Bridge1 {

    public static void main(String[] args) {
        Shape c1 = new Circle(new VectorRenderer(), 5);
        Shape c2 = new Circle(new RasterRenderer(), 5);
        c1.draw();
        c2.draw();
    }
}

interface Renderer {

    void renderCircle(float r);
}

class VectorRenderer implements Renderer {

    @Override
    public void renderCircle(float r) {
        System.out.println("Drawing vector circle of radius " + r);

    }
}

class RasterRenderer implements Renderer {

    @Override
    public void renderCircle(float r) {
        System.out.println("Drawing raster circle of radius " + r);

    }
}

abstract class Shape {

    protected Renderer renderer;

    public Shape(Renderer renderer) {
        this.renderer = renderer;
    }

    public abstract void draw();
}

class Circle extends Shape {

    private float radius;

    public Circle(Renderer renderer, float radius) {
        super(renderer);
        this.radius = radius;
    }

    @Override
    public void draw() {
        renderer.renderCircle(radius);
    }
}
