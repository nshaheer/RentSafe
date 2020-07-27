package com.leaseguard.leaseguard.models;

import java.util.UUID;

public class LeaseDocument {
    private String title;
    private String address;
    private int rent;
    private String dateRange;
    private int numIssues;
    private String uuid;

    public LeaseDocument(String title, String address, int rent, String dateRange, int numIssues) {
        this.title = title;
        this.address = address;
        this.rent = rent;
        this.dateRange = dateRange;
        this.numIssues = numIssues;
        this.uuid = UUID.randomUUID().toString();
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

    public String getUuid() { return uuid; }
}
