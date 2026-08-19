// Product Class
class TravelPlan {
    private String transportation;
    private String accommodation;
    private String dailyActivities;

    public void setTransportation(String transportation) {
        this.transportation = transportation;
    }

    public void setAccommodation(String accommodation) {
        this.accommodation = accommodation;
    }

    public void setDailyActivities(String dailyActivities) {
        this.dailyActivities = dailyActivities;
    }

    @Override
    public String toString() {
        return "TravelPlan [" +
                "Transportation='" + transportation + '\'' +
                ", Accommodation='" + accommodation + '\'' +
                ", Activities='" + dailyActivities + '\'' +
                ']';
    }
}

// Abstract Builder Interface
interface TravelPlanBuilder {
    void buildTransportation();
    void buildAccommodation();
    void buildDailyActivities();
    TravelPlan getPlan();
}

// Concrete Builder: Luxury Plan
class LuxuryPlanBuilder implements TravelPlanBuilder {
    private TravelPlan plan;

    public LuxuryPlanBuilder() {
        this.plan = new TravelPlan();
    }

    @Override
    public void buildTransportation() {
        plan.setTransportation("Business Class Flight");
    }

    @Override
    public void buildAccommodation() {
        plan.setAccommodation("Luxury Hotel");
    }

    @Override
    public void buildDailyActivities() {
        plan.setDailyActivities("Private City Tour");
    }

    @Override
    public TravelPlan getPlan() {
        return this.plan;
    }
}

// Concrete Builder: Budget Plan
class BudgetPlanBuilder implements TravelPlanBuilder {
    private TravelPlan plan;

    public BudgetPlanBuilder() {
        this.plan = new TravelPlan();
    }

    @Override
    public void buildTransportation() {
        plan.setTransportation("Economy Bus");
    }

    @Override
    public void buildAccommodation() {
        plan.setAccommodation("Hostel");
    }

    @Override
    public void buildDailyActivities() {
        plan.setDailyActivities("Group Walking Tour");
    }

    @Override
    public TravelPlan getPlan() {
        return this.plan;
    }
}

// Director Class
class TravelPlanDirector {
    private TravelPlanBuilder builder;

    public TravelPlanDirector(TravelPlanBuilder builder) {
        this.builder = builder;
    }

    public void constructPlan() {
        builder.buildTransportation();
        builder.buildAccommodation();
        builder.buildDailyActivities();
    }

    public TravelPlan getTravelPlan() {
        return builder.getPlan();
    }
}

// Client Code
public class Solution {
    public static void main(String[] args) {
        // Constructing a Luxury Plan
        TravelPlanBuilder luxuryBuilder = new LuxuryPlanBuilder();
        TravelPlanDirector luxuryDirector = new TravelPlanDirector(luxuryBuilder);
        luxuryDirector.constructPlan();
        TravelPlan luxuryPlan = luxuryDirector.getTravelPlan();
        System.out.println(luxuryPlan);

        // Constructing a Budget Plan
        TravelPlanBuilder budgetBuilder = new BudgetPlanBuilder();
        TravelPlanDirector budgetDirector = new TravelPlanDirector(budgetBuilder);
        budgetDirector.constructPlan();
        TravelPlan budgetPlan = budgetDirector.getTravelPlan();
        System.out.println(budgetPlan);
    }
}