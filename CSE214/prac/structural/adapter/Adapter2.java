public class Adapter2 {
    public static void main(String[] args) {
        RoundHole hole = new RoundHole(5);
        RoundPeg rpeg = new RoundPeg(5);

        if(hole.fits(rpeg)) System.out.println("rpeg r5 fits into hole r5");
        
        SquarePeg smallSquarePeg = new SquarePeg(2);
        SquarePeg largeSquarePeg = new SquarePeg(20);

        SquarePegAdapter smallSquarePegAdapter = new SquarePegAdapter(smallSquarePeg);
        SquarePegAdapter largeSquarePegAdapter = new SquarePegAdapter(largeSquarePeg);

        if(hole.fits(smallSquarePegAdapter)) System.out.println("Sqpeg w2 fits into hole r5");
        if(!hole.fits(largeSquarePegAdapter)) System.out.println("Sqpeg w20 does NOT fit into hole r5");
        
    }
}

class RoundHole {
    private double radius;

    public RoundHole(double radius) {
        this.radius = radius;
    }

    public double getRadius() {return radius;}

    public boolean fits(RoundPeg peg) {return this.getRadius() >= peg.getRadius();}
}

class RoundPeg {
    private double radius;

    public RoundPeg() { }

    public RoundPeg(double radius) {
        this.radius = radius;
    }

    public double getRadius() {return radius;}
    
}

class SquarePeg {
    private double width;
    
    public SquarePeg() { }

    public SquarePeg(double width) {
        this.width = width;
    }

    public double getArea() {return width * width;}
    
}

class SquarePegAdapter extends RoundPeg {
    private SquarePeg peg;

    public SquarePegAdapter(SquarePeg peg) {
        this.peg = peg;
    }

    @Override
    public double getRadius() {
        return Math.sqrt(Math.pow((peg.getArea() / 2), 2) * 2);
    }

}