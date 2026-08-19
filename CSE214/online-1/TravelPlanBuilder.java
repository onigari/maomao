public class TravelPlanBuilder implements Builder {
    
    Plan plan = new Plan();

    @Override
    public Builder reset() {
        plan = new Plan();
        return this;
    }
@Override
    public Builder setTransport(String transport) {
        plan.setTransport(transport);
        return this;
    }
@Override
    public Builder setAccomodation(String accomodation) {
        plan.setAccomodation(accomodation);
        return this;
    }

    @Override
    public Builder setTour(String tour) {
        plan.setTour(tour);
        return this;
    }


    public Plan getTravelPlan() {
        return plan;
    }
}