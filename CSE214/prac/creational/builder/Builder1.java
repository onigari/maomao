
public class Builder1 {

    public static void main(String[] args) {
        HouseBuilder builder = new WoodenHouseBuilder();
        // House house = new WoodenHouseBuilder().buildFoundation().buildWalls().buildRoof().getResult();
        Director director = new Director(builder);
        director.constructHouse();
        House house = builder.getResult();
    }
}

class House {

    private String foundation, walls, roof;

    public void foundation(String foundation) {
        this.foundation = foundation;
    }

    public void walls(String walls) {
        this.walls = walls;
    }

    public void roof(String roof) {
        this.roof = roof;
    }
}

interface HouseBuilder {
    HouseBuilder buildFoundation();
    HouseBuilder buildWalls();
    HouseBuilder buildRoof();
    House getResult();
}

class WoodenHouseBuilder implements HouseBuilder {
    private House house = new House();

    @Override
    public HouseBuilder buildFoundation() {
        house.foundation("Wood posts");
        System.out.println("Building...");
        return this;
    }
    @Override
    public HouseBuilder buildWalls() {
        house.walls("Wooden planks");
        System.out.println("Building...");
        return this;
    }
    @Override
    public HouseBuilder buildRoof() {
        house.roof("Shingle roof");
        System.out.println("Building...");
        return this;
    }

    @Override
    public House getResult() {
        return house;
    }
    
}


class Director {
    private HouseBuilder builder;
    public Director(HouseBuilder builder) {this.builder = builder;}

    public void constructHouse() {
        builder.buildFoundation();
        builder.buildWalls();
        builder.buildRoof();
    }
}