
public class Example2 {

    public static void main(String[] args) {
        Restaurant r = new BeefBurgerRestaurant();
        r.orderBurger();
    }
}

abstract class Restaurant {

    public void orderBurger() {
        Burger burger = createBurger();

        burger.prepare();
    }

    public abstract Burger createBurger();
}

class BeefBurgerRestaurant extends Restaurant {

    @Override
    public Burger createBurger() {
        return new BeefBurger();
    }
}

class VeggieBurgerRestaurant extends Restaurant {

    @Override
    public Burger createBurger() {
        return new VeggieBurger();
    }
}

interface Burger {

    void prepare();
}

class BeefBurger implements Burger {

    @Override
    public void prepare() {
        System.out.println("Prepareing beef burger");
    }

}

class VeggieBurger implements Burger {

    @Override
    public void prepare() {
        System.out.println("Prepareing veggie burger");
    }

}
