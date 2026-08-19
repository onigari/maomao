import java.util.ArrayList;
import java.util.List;

// ==========================================
// 1. COMPOSITE PATTERN: Items and Packages
// ==========================================

// Base Component
interface GiftComponent {
    double getCost();
    void display(String indent);
}

// Leaf Component (Individual Gift Item)
class GiftItem implements GiftComponent {
    private String name;
    private double price;

    public GiftItem(String name, double price) {
        this.name = name;
        this.price = price;
    }

    @Override
    public double getCost() {
        return price;
    }

    @Override
    public void display(String indent) {
        System.out.println(indent + "- Item: " + name + " ($" + price + ")");
    }
}

// ==========================================
// 2. BRIDGE PATTERN: Packaging Styles
// ==========================================

// Implementor Interface (Packaging Style)
interface PackagingStyle {
    double getPackagingCost();
    String getPresentationStyle();
}

// Concrete Implementors
class StandardGiftBox implements PackagingStyle {
    @Override
    public double getPackagingCost() { return 0.0; }
    
    @Override
    public String getPresentationStyle() { return "Standard Gift Box"; }
}

class PremiumGiftBox implements PackagingStyle {
    @Override
    public double getPackagingCost() { return 15.0; }
    
    @Override
    public String getPresentationStyle() { return "Premium Wrapping with Decorative Ribbon"; }
}

class EcoFriendlyGiftBox implements PackagingStyle {
    @Override
    public double getPackagingCost() { return 8.0; }
    
    @Override
    public String getPresentationStyle() { return "Eco-Friendly Recyclable Materials"; }
}

// ==========================================
// 3. COMBINING COMPOSITE AND BRIDGE
// ==========================================

// Composite & Abstraction
abstract class GiftPackage implements GiftComponent {
    protected String packageName;
    protected String creatorName;
    protected PackagingStyle packagingStyle; // Bridge reference
    protected List<GiftComponent> components = new ArrayList<>();

    public GiftPackage(String packageName, String creatorName, PackagingStyle packagingStyle) {
        this.packageName = packageName;
        this.creatorName = creatorName;
        this.packagingStyle = packagingStyle;
    }

    public void addComponent(GiftComponent component) {
        components.add(component);
    }

    public void removeComponent(GiftComponent component) {
        components.remove(component);
    }

    @Override
    public double getCost() {
        double totalCost = packagingStyle.getPackagingCost();
        for (GiftComponent component : components) {
            totalCost += component.getCost();
        }
        return totalCost;
    }

    @Override
    public void display(String indent) {
        System.out.println(indent + "=== Package: " + packageName + " ===");
        System.out.println(indent + "Creator: " + creatorName);
        System.out.println(indent + "Type: " + getTargetAudience());
        System.out.println(indent + "Packaging: " + packagingStyle.getPresentationStyle() + 
                           " (+$" + packagingStyle.getPackagingCost() + ")");
        System.out.println(indent + "Contents:");
        
        for (GiftComponent component : components) {
            component.display(indent + "  ");
        }
        System.out.println(indent + "-> Total Cost of '" + packageName + "': $" + getCost() + "\n");
    }

    // Hook for refined abstractions
    protected abstract String getTargetAudience();
}

// Refined Abstractions
class PersonalGiftPackage extends GiftPackage {
    public PersonalGiftPackage(String packageName, String creatorName, PackagingStyle packagingStyle) {
        super(packageName, creatorName, packagingStyle);
    }

    @Override
    protected String getTargetAudience() {
        return "Personal (Individual Recipient)";
    }
}

class CorporateGiftPackage extends GiftPackage {
    public CorporateGiftPackage(String packageName, String creatorName, PackagingStyle packagingStyle) {
        super(packageName, creatorName, packagingStyle);
    }

    @Override
    protected String getTargetAudience() {
        return "Corporate (Organization Employees)";
    }
}

// ==========================================
// 4. CLIENT CODE
// ==========================================

public class B1 {
    public static void main(String[] args) {
        // 1. Create Individual Items
        GiftComponent chocolates = new GiftItem("Gourmet Chocolates", 20.0);
        GiftComponent mug = new GiftItem("Coffee Mug", 10.0);
        GiftComponent perfume = new GiftItem("Luxury Perfume", 55.0);
        GiftComponent book = new GiftItem("Bestseller Novel", 15.0);

        // 2. Create a Company Predefined Package (Standard Box)
        GiftPackage companyCoffeeBundle = new CorporateGiftPackage(
                "Morning Coffee Bundle", 
                "Company Admin", 
                new StandardGiftBox()
        );
        companyCoffeeBundle.addComponent(chocolates);
        companyCoffeeBundle.addComponent(mug);

        // 3. Create a User-Crafted Personal Package (Premium Box)
        // This package contains individual items AND the predefined package above
        GiftPackage userAnniversaryGift = new PersonalGiftPackage(
                "Happy Anniversary", 
                "John Doe", 
                new PremiumGiftBox()
        );
        userAnniversaryGift.addComponent(perfume);
        userAnniversaryGift.addComponent(book);
        userAnniversaryGift.addComponent(companyCoffeeBundle); // Nesting a package inside a package

        // 4. Display the deeply nested user package
        userAnniversaryGift.display("");
    }
}