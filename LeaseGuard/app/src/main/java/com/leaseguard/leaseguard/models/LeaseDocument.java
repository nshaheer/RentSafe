package com.leaseguard.leaseguard.models;

public class LeaseDocument {
    private String title;
    private String address;
    private int rent;
    private String dateRange;
    private int numIssues;

    public LeaseDocument(String title, String address, int rent, String dateRange, int numIssues) {
        this.title = title;
        this.address = address;
        this.rent = rent;
        this.dateRange = dateRange;
        this.numIssues = numIssues;
    }

    public String getTitle() {
        return title;
    }

    public String getAddress() {
        return address;
    }

    public int getRent() {
        return rent;
    }

    public String getDateRange() {
        return dateRange;
    }

    public int getNumIssues() {
        return numIssues;
    }
}
