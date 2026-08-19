// ==========================================
// 1. DECORATOR PATTERN: Gift and Wrapping
// ==========================================

// Base Component
interface Gift {
    double getPrice();
    String getDescription();
}

// Concrete Component
class BaseGift implements Gift {
    private String description;
    private double basePrice;

    public BaseGift(String description, double basePrice) {
        this.description = description;
        this.basePrice = basePrice;
    }

    @Override
    public double getPrice() {
        return basePrice;
    }

    @Override
    public String getDescription() {
        return description;
    }
}

// Decorator
abstract class GiftDecorator implements Gift {
    protected Gift wrappedGift;

    public GiftDecorator(Gift wrappedGift) {
        this.wrappedGift = wrappedGift;
    }
}

// Concrete Decorator
class WrappedGift extends GiftDecorator {
    public WrappedGift(Gift wrappedGift) {
        super(wrappedGift);
    }

    @Override
    public double getPrice() {
        return wrappedGift.getPrice() + 2.0; // Adds $2 for wrapping
    }

    @Override
    public String getDescription() {
        return wrappedGift.getDescription() + " (with Gift Wrapping)";
    }
}

// ==========================================
// 2. BRIDGE PATTERN: Delivery Regions & Modes
// ==========================================

// Implementor Interface (Delivery Mode)
interface DeliveryMode {
    double getModeSurcharge();
    String getEstimatedTime(String regionType);
}

// Concrete Implementors
class StandardDelivery implements DeliveryMode {
    @Override
    public double getModeSurcharge() {
        return 0.0;
    }

    @Override
    public String getEstimatedTime(String regionType) {
        switch (regionType) {
            case "LOCAL": return "1 week";
            case "NATIONAL": return "1-2 weeks";
            case "INTERNATIONAL": return "2-3 weeks";
            default: return "Unknown";
        }
    }
}

class ExpressDelivery implements DeliveryMode {
    @Override
    public double getModeSurcharge() {
        return 10.0; // Adds $10
    }

    @Override
    public String getEstimatedTime(String regionType) {
        if (regionType.equals("INTERNATIONAL")) {
            return "1 week";
        }
        return "2 days";
    }
}

class PriorityDelivery implements DeliveryMode {
    @Override
    public double getModeSurcharge() {
        return 25.0; // Adds $25
    }

    @Override
    public String getEstimatedTime(String regionType) {
        if (regionType.equals("INTERNATIONAL")) {
            return "5 days";
        }
        return "1 day";
    }
}

// Abstraction (Delivery Region)
abstract class DeliveryRegion {
    protected DeliveryMode deliveryMode;
    protected double distance;

    public DeliveryRegion(DeliveryMode deliveryMode, double distance) {
        this.deliveryMode = deliveryMode;
        this.distance = distance;
    }

    public abstract double getDeliveryCost();
    public abstract String getDeliveryTime();
}

// Concrete Abstractions
class LocalDelivery extends DeliveryRegion {
    public LocalDelivery(DeliveryMode deliveryMode, double distance) {
        super(deliveryMode, distance);
    }

    @Override
    public double getDeliveryCost() {
        return (distance * 1.0) + deliveryMode.getModeSurcharge();
    }

    @Override
    public String getDeliveryTime() {
        return deliveryMode.getEstimatedTime("LOCAL");
    }
}

class NationalDelivery extends DeliveryRegion {
    public NationalDelivery(DeliveryMode deliveryMode, double distance) {
        super(deliveryMode, distance);
    }

    @Override
    public double getDeliveryCost() {
        return (distance * 1.0) + 20.0 + deliveryMode.getModeSurcharge();
    }

    @Override
    public String getDeliveryTime() {
        return deliveryMode.getEstimatedTime("NATIONAL");
    }
}

class InternationalDelivery extends DeliveryRegion {
    public InternationalDelivery(DeliveryMode deliveryMode) {
        super(deliveryMode, 0); // Distance not applicable for international fixed rate
    }

    @Override
    public double getDeliveryCost() {
        return 500.0 + deliveryMode.getModeSurcharge();
    }

    @Override
    public String getDeliveryTime() {
        return deliveryMode.getEstimatedTime("INTERNATIONAL");
    }
}

// ==========================================
// 3. ORDER PROCESSOR & CLIENT
// ==========================================

class Order {
    private Gift gift;
    private DeliveryRegion delivery;

    public Order(Gift gift, DeliveryRegion delivery) {
        this.gift = gift;
        this.delivery = delivery;
    }

    public void printOrderSummary(String caseName) {
        double totalCost = gift.getPrice() + (delivery != null ? delivery.getDeliveryCost() : 0);
        String time = (delivery != null) ? delivery.getDeliveryTime() : "N/A";
        
        System.out.println("--- " + caseName + " ---");
        System.out.println("Item: " + gift.getDescription());
        System.out.println("Total Cost: $" + (int) totalCost);
        System.out.println("Estimated Delivery Time: " + time + "\n");
    }
}

public class A1 {
    public static void main(String[] args) {
        
        // Case 1: $40 decorative vase, 10 miles local, gift wrapped, standard delivery
        Gift vase = new BaseGift("Decorative Vase", 40.0);
        vase = new WrappedGift(vase);
        DeliveryRegion localDelivery = new LocalDelivery(new StandardDelivery(), 10.0);
        Order case1 = new Order(vase, localDelivery);
        case1.printOrderSummary("Case 1");

        // Case 2: $60 wooden souvenir, 50 miles national, gift wrapped, Express delivery
        Gift souvenir = new BaseGift("Wooden Souvenir", 60.0);
        souvenir = new WrappedGift(souvenir);
        DeliveryRegion nationalDelivery = new NationalDelivery(new ExpressDelivery(), 50.0);
        Order case2 = new Order(souvenir, nationalDelivery);
        case2.printOrderSummary("Case 2");

        // Case 3: $150 crystal showpiece, international, Priority delivery (no wrapping)
        Gift showpiece = new BaseGift("Crystal Showpiece", 150.0);
        DeliveryRegion internationalDelivery = new InternationalDelivery(new PriorityDelivery());
        Order case3 = new Order(showpiece, internationalDelivery);
        case3.printOrderSummary("Case 3");
    }
}