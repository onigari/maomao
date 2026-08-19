
public class Decorator1 {

    public static void main(String[] args) {
        Coffee myCoffee = new SimpleCoffee();
        myCoffee = new MilkDecorator(myCoffee);
        myCoffee = new SugarDecorator(myCoffee);
        System.out.println(myCoffee.getDescription());
        System.out.println(myCoffee.getCost());

    }
}

interface Coffee {

    String getDescription();

    double getCost();
}

class SimpleCoffee implements Coffee {
    
    @Override
    public String getDescription() {
        return "Simple coffee";
    }

    @Override
    public double getCost() {
        return 1.0;
    }
}

abstract class CoffeeDecorator implements Coffee {

    protected Coffee wrappee;

    public CoffeeDecorator(Coffee coffee) {
        this.wrappee = coffee;
    }

    @Override
    public String getDescription() {
        return wrappee.getDescription();
    }

    @Override
    public double getCost() {
        return wrappee.getCost();
    }

}

class MilkDecorator extends CoffeeDecorator {

    public MilkDecorator(Coffee coffee) {
        super(coffee);
    }

    @Override
    public String getDescription() {
        return wrappee.getDescription() + ", Milk";
    }

    @Override
    public double getCost() {
        return wrappee.getCost() + 0.25;
    }

}

class SugarDecorator extends CoffeeDecorator {

    public SugarDecorator(Coffee coffee) {
        super(coffee);
    }

    @Override
    public String getDescription() {
        return wrappee.getDescription() + ", Sugar";

    }

    @Override
    public double getCost() {
        return wrappee.getCost() + 0.10;

    }

}
