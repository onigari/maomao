public class Director {
    void createLuxuryPlan(TravelPlanBuilder builder) {
        builder.setTransport("Business Class Flight").setAccomodation("Luxury Hotel").setTour("Private City Tour");
    }

    void createBudgetPlan(TravelPlanBuilder builder) {
        builder.reset().setTransport("Economy Bus").setAccomodation("Hostel").setTour("Group Walking Tour");
    }
}
