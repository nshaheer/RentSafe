extraction_job_results = [
    "Lease for Unit _1603_ at 333 King St. North, Waterloo",
    "Dated the __16th__ day of __April______ A.D. 2012 made pursuant to the provisions of the Tenant Protection Act",
    "BETWEEN:",
    "Rise Real Estate Inc.",
    "611 Tradewind Drive, Suite 300",
    "Ancaster, ON L9G 4V5",
    "Fax: (888) 267-7659",
    "Web: www.luxewaterloo.com",
    "RENTED PREMISES",
    "1. a) The Landlord agrees to rent to the Tenant and the Tenant agrees to rent from the Landlord (hereinafter referred to",
    "as the rented premises)",
    "PARKING COVENANTS",
    "2. In order to secure a parking spot, the Tenant must fill out and sign the Parking Agreement form. Parking is available on",
    "a first-come first-served basis. The Tenant agrees to abide by the covenants, agreements, rules and regulations of this",
    "Agreement; it is agreed that the Landlord shall have the same remedies as in the case of nonpayment of rent in the event",
    "of a breach of performance by the Tenant of any of the terms and conditions of this agreement.",
    "TERM",
    "3. The Tenant will occupy the rented premises, subject to the present tenant vacating, for the term beginning the 1st day",
    "of May A.D. 2013 and ending on the 30th day of April A.D. 2014 subject to the terms of this Agreement.",
    "In the event that the building is under construction or under substantial renovation, the date of occupancy may be",
    "deferred and the tenure of this lease extended accordingly, upon 10 days written notice to the tenant.",
    "RENT",
    "4. a) The Tenant agrees to pay to the Landlord, at the Landlord's office or such place as directed in writing from time to",
    "time by the Landlord only:",
    "For Rented Premises $ monthly",
    "Lease for Unit _1603_ at 333 King St. North, Waterloo",
    "· ___Aleem Dhanji__________________________ ·",
    "____________________________________________ ·",
    "____________________________________________ ·",
    "____________________________________________",
    "(The Tenants)",
    "Unit _1603__ at 333 King St. North, Waterloo, Ontario",
    "Dated the __16th__ day of __April______ A.D. 2012 made pursuant to the provisions of the Tenant Protection Act.",
    "____600________",
    "on the FIRST day of every month during the term described above, yielding and paying thereafter during the said term",
    "and hereby granting unto the Landlord, its successors, the assigns, the sum of $___7200___ yearly (hereinafter called",
    "No pets are allowed on the lease premises or any part of the building , unless consented",
    "No guests of the Tenant are to reside in or remain on the premises for a period of longer than two weeks without the prior registration of that guest with the Landlord or its agent. Registration of a guest shall not be deemed to constitute the Landlord's consent to an assignment of this Lease or a sub-letting thereof.",
    "No guests of the Tenants may occupy the Premises for longer than one week without the prior written consent of the Landlord.",
]

recog_job_results = [
    {
        "Entities": [
            {
                "BeginOffset": 25,
                "EndOffset": 43,
                "Score": 0.7787701796741324,
                "Text": "333 King St. North",
                "Type": "LOCATION",
            },
            {
                "BeginOffset": 45,
                "EndOffset": 53,
                "Score": 0.9123940061154407,
                "Text": "Waterloo",
                "Type": "LOCATION",
            },
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 0,
    },
    {
        "Entities": [
            {
                "BeginOffset": 45,
                "EndOffset": 49,
                "Score": 0.5593858748479517,
                "Text": "2012",
                "Type": "DATE",
            },
            {
                "BeginOffset": 89,
                "EndOffset": 110,
                "Score": 0.9998348184711828,
                "Text": "Tenant Protection Act",
                "Type": "TITLE",
            },
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 1,
    },
    {
        "Entities": [
            {
                "BeginOffset": 0,
                "EndOffset": 7,
                "Score": 0.4135950218839568,
                "Text": "BETWEEN",
                "Type": "TITLE",
            }
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 2,
    },
    {
        "Entities": [
            {
                "BeginOffset": 0,
                "EndOffset": 21,
                "Score": 0.9890634490017918,
                "Text": "Rise Real Estate Inc.",
                "Type": "ORGANIZATION",
            }
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 3,
    },
    {
        "Entities": [
            {
                "BeginOffset": 0,
                "EndOffset": 19,
                "Score": 0.7657328251615962,
                "Text": "611 Tradewind Drive",
                "Type": "COMMERCIAL_ITEM",
            },
            {
                "BeginOffset": 21,
                "EndOffset": 30,
                "Score": 0.5048164774758519,
                "Text": "Suite 300",
                "Type": "COMMERCIAL_ITEM",
            },
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 4,
    },
    {
        "Entities": [
            {
                "BeginOffset": 0,
                "EndOffset": 8,
                "Score": 0.9847062304394081,
                "Text": "Ancaster",
                "Type": "LOCATION",
            },
            {
                "BeginOffset": 10,
                "EndOffset": 12,
                "Score": 0.6221848580990165,
                "Text": "ON",
                "Type": "OTHER",
            },
            {
                "BeginOffset": 13,
                "EndOffset": 20,
                "Score": 0.6730422596702678,
                "Text": "L9G 4V5",
                "Type": "COMMERCIAL_ITEM",
            },
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 5,
    },
    {
        "Entities": [
            {
                "BeginOffset": 5,
                "EndOffset": 19,
                "Score": 0.9995650194436332,
                "Text": "(888) 267-7659",
                "Type": "OTHER",
            }
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 6,
    },
    {
        "Entities": [
            {
                "BeginOffset": 5,
                "EndOffset": 25,
                "Score": 0.9987712717548388,
                "Text": "www.luxewaterloo.com",
                "Type": "OTHER",
            }
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 7,
    },
    {"Entities": [], "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt", "Line": 8},
    {
        "Entities": [
            {
                "BeginOffset": 0,
                "EndOffset": 2,
                "Score": 0.7840577835385479,
                "Text": "1.",
                "Type": "QUANTITY",
            }
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 9,
    },
    {"Entities": [], "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt", "Line": 10},
    {"Entities": [], "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt", "Line": 11},
    {
        "Entities": [
            {
                "BeginOffset": 0,
                "EndOffset": 1,
                "Score": 0.8030085516494962,
                "Text": "2",
                "Type": "QUANTITY",
            }
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 12,
    },
    {
        "Entities": [
            {
                "BeginOffset": 13,
                "EndOffset": 18,
                "Score": 0.5857338592725574,
                "Text": "first",
                "Type": "QUANTITY",
            }
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 13,
    },
    {"Entities": [], "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt", "Line": 14},
    {"Entities": [], "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt", "Line": 15},
    {"Entities": [], "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt", "Line": 16},
    {
        "Entities": [
            {
                "BeginOffset": 0,
                "EndOffset": 1,
                "Score": 0.7723815298651419,
                "Text": "3",
                "Type": "QUANTITY",
            },
            {
                "BeginOffset": 114,
                "EndOffset": 121,
                "Score": 0.9855108300487536,
                "Text": "1st day",
                "Type": "QUANTITY",
            },
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 17,
    },
    {
        "Entities": [
            {
                "BeginOffset": 3,
                "EndOffset": 16,
                "Score": 0.9760405569318982,
                "Text": "May A.D. 2013",
                "Type": "DATE",
            },
            {
                "BeginOffset": 35,
                "EndOffset": 62,
                "Score": 0.9314047789112536,
                "Text": "30th day of April A.D. 2014",
                "Type": "DATE",
            },
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 18,
    },
    {"Entities": [], "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt", "Line": 19},
    {
        "Entities": [
            {
                "BeginOffset": 65,
                "EndOffset": 72,
                "Score": 0.9993503204163455,
                "Text": "10 days",
                "Type": "QUANTITY",
            }
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 20,
    },
    {"Entities": [], "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt", "Line": 21},
    {
        "Entities": [
            {
                "BeginOffset": 0,
                "EndOffset": 2,
                "Score": 0.9634377623228836,
                "Text": "4.",
                "Type": "QUANTITY",
            }
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 22,
    },
    {"Entities": [], "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt", "Line": 23},
    {
        "Entities": [
            {
                "BeginOffset": 20,
                "EndOffset": 21,
                "Score": 0.9679296724215092,
                "Text": "$",
                "Type": "QUANTITY",
            },
            {
                "BeginOffset": 22,
                "EndOffset": 29,
                "Score": 0.854935729603293,
                "Text": "monthly",
                "Type": "QUANTITY",
            },
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 24,
    },
    {
        "Entities": [
            {
                "BeginOffset": 25,
                "EndOffset": 43,
                "Score": 0.7787701796741324,
                "Text": "333 King St. North",
                "Type": "LOCATION",
            },
            {
                "BeginOffset": 45,
                "EndOffset": 53,
                "Score": 0.9123940061154407,
                "Text": "Waterloo",
                "Type": "LOCATION",
            },
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 25,
    },
    {
        "Entities": [
            {
                "BeginOffset": 11,
                "EndOffset": 43,
                "Score": 0.9996071213818376,
                "Text": "Dhanji__________________________",
                "Type": "PERSON",
            }
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 26,
    },
    {"Entities": [], "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt", "Line": 27},
    {"Entities": [], "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt", "Line": 28},
    {"Entities": [], "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt", "Line": 29},
    {
        "Entities": [
            {
                "BeginOffset": 1,
                "EndOffset": 12,
                "Score": 0.9990961796297617,
                "Text": "The Tenants",
                "Type": "TITLE",
            }
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 30,
    },
    {
        "Entities": [
            {
                "BeginOffset": 16,
                "EndOffset": 53,
                "Score": 0.979470600710061,
                "Text": "333 King St. North, Waterloo, Ontario",
                "Type": "LOCATION",
            }
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 31,
    },
    {
        "Entities": [
            {
                "BeginOffset": 45,
                "EndOffset": 49,
                "Score": 0.5842071754333343,
                "Text": "2012",
                "Type": "DATE",
            },
            {
                "BeginOffset": 89,
                "EndOffset": 110,
                "Score": 0.9998270764696474,
                "Text": "Tenant Protection Act",
                "Type": "TITLE",
            },
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 32,
    },
    {"Entities": [], "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt", "Line": 33},
    {
        "Entities": [
            {
                "BeginOffset": 7,
                "EndOffset": 16,
                "Score": 0.9994990007280317,
                "Text": "FIRST day",
                "Type": "QUANTITY",
            },
            {
                "BeginOffset": 20,
                "EndOffset": 31,
                "Score": 0.9262160013177787,
                "Text": "every month",
                "Type": "QUANTITY",
            },
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 34,
    },
    {
        "Entities": [
            {
                "BeginOffset": 79,
                "EndOffset": 80,
                "Score": 0.9745091623593639,
                "Text": "$",
                "Type": "QUANTITY",
            }
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 35,
    },
    {"Entities": [], "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt", "Line": 36},
    {
        "Entities": [
            {
                "BeginOffset": 95,
                "EndOffset": 104,
                "Score": 0.9930840922664373,
                "Text": "two weeks",
                "Type": "QUANTITY",
            }
        ],
        "File": "53f2604a-c929-441f-9f8e-79aaafff66bc.txt",
        "Line": 37,
    },
]

classification_job_results = [
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "0",
        "Classes": [
            {"Name": "Other", "Score": 0.4526},
            {"Name": "Guests Prohibited", "Score": 0.1217},
            {"Name": "Security Deposit", "Score": 0.1208},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "1",
        "Classes": [
            {"Name": "Other", "Score": 0.7952},
            {"Name": "Security Deposit", "Score": 0.0752},
            {"Name": "Key Deposit", "Score": 0.0344},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "2",
        "Classes": [
            {"Name": "Other", "Score": 0.197},
            {"Name": "Guests Prohibited", "Score": 0.187},
            {"Name": "Rent Deposit", "Score": 0.181},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "3",
        "Classes": [
            {"Name": "Other", "Score": 0.2125},
            {"Name": "Security Deposit", "Score": 0.1978},
            {"Name": "Guests Prohibited", "Score": 0.1715},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "4",
        "Classes": [
            {"Name": "Other", "Score": 0.1914},
            {"Name": "Security Deposit", "Score": 0.1881},
            {"Name": "Rent Deposit", "Score": 0.1708},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "5",
        "Classes": [
            {"Name": "Guests Prohibited", "Score": 0.2116},
            {"Name": "Other", "Score": 0.1814},
            {"Name": "Rent Deposit", "Score": 0.1626},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "6",
        "Classes": [
            {"Name": "Other", "Score": 0.2173},
            {"Name": "Guests Prohibited", "Score": 0.1816},
            {"Name": "Rent Deposit", "Score": 0.1767},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "7",
        "Classes": [
            {"Name": "Other", "Score": 0.2164},
            {"Name": "Guests Prohibited", "Score": 0.189},
            {"Name": "Rent Deposit", "Score": 0.1648},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "8",
        "Classes": [
            {"Name": "Other", "Score": 0.236},
            {"Name": "Rent Deposit", "Score": 0.187},
            {"Name": "Guests Prohibited", "Score": 0.1809},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "9",
        "Classes": [
            {"Name": "Other", "Score": 0.9264},
            {"Name": "Rent Deposit", "Score": 0.0225},
            {"Name": "Pets Prohibited", "Score": 0.0148},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "10",
        "Classes": [
            {"Name": "Other", "Score": 0.4047},
            {"Name": "Rent Deposit", "Score": 0.1937},
            {"Name": "Security Deposit", "Score": 0.125},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "11",
        "Classes": [
            {"Name": "Other", "Score": 0.2144},
            {"Name": "Guests Prohibited", "Score": 0.1906},
            {"Name": "Security Deposit", "Score": 0.1674},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "12",
        "Classes": [
            {"Name": "Other", "Score": 0.7786},
            {"Name": "Security Deposit", "Score": 0.056},
            {"Name": "Key Deposit", "Score": 0.0518},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "13",
        "Classes": [
            {"Name": "Other", "Score": 0.7693},
            {"Name": "Pets Prohibited", "Score": 0.0699},
            {"Name": "Rent Deposit", "Score": 0.0484},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "14",
        "Classes": [
            {"Name": "Other", "Score": 0.9045},
            {"Name": "Rent Deposit", "Score": 0.0252},
            {"Name": "Guests Prohibited", "Score": 0.0247},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "15",
        "Classes": [
            {"Name": "Other", "Score": 0.6299},
            {"Name": "Pets Prohibited", "Score": 0.1126},
            {"Name": "Rent Deposit", "Score": 0.1109},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "16",
        "Classes": [
            {"Name": "Guests Prohibited", "Score": 0.2091},
            {"Name": "Security Deposit", "Score": 0.1865},
            {"Name": "Rent Deposit", "Score": 0.1699},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "17",
        "Classes": [
            {"Name": "Other", "Score": 0.8842},
            {"Name": "Rent Deposit", "Score": 0.0378},
            {"Name": "Guests Prohibited", "Score": 0.02},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "18",
        "Classes": [
            {"Name": "Other", "Score": 0.6908},
            {"Name": "Pets Prohibited", "Score": 0.0894},
            {"Name": "Rent Deposit", "Score": 0.0811},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "19",
        "Classes": [
            {"Name": "Other", "Score": 0.6964},
            {"Name": "Pets Prohibited", "Score": 0.0791},
            {"Name": "Security Deposit", "Score": 0.0732},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "20",
        "Classes": [
            {"Name": "Other", "Score": 0.754},
            {"Name": "Guests Prohibited", "Score": 0.0578},
            {"Name": "Security Deposit", "Score": 0.0577},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "21",
        "Classes": [
            {"Name": "Rent Deposit", "Score": 0.2645},
            {"Name": "Other", "Score": 0.1801},
            {"Name": "Security Deposit", "Score": 0.1777},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "22",
        "Classes": [
            {"Name": "Other", "Score": 0.9326},
            {"Name": "Rent Deposit", "Score": 0.0231},
            {"Name": "Security Deposit", "Score": 0.0145},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "23",
        "Classes": [
            {"Name": "Other", "Score": 0.3949},
            {"Name": "Rent Deposit", "Score": 0.1617},
            {"Name": "Security Deposit", "Score": 0.1491},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "24",
        "Classes": [
            {"Name": "Other", "Score": 0.2758},
            {"Name": "Rent Deposit", "Score": 0.2286},
            {"Name": "Security Deposit", "Score": 0.148},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "25",
        "Classes": [
            {"Name": "Other", "Score": 0.4526},
            {"Name": "Guests Prohibited", "Score": 0.1217},
            {"Name": "Security Deposit", "Score": 0.1208},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "26",
        "Classes": [
            {"Name": "Other", "Score": 0.3045},
            {"Name": "Rent Deposit", "Score": 0.1494},
            {"Name": "Security Deposit", "Score": 0.1459},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "27",
        "Classes": [
            {"Name": "Other", "Score": 0.2652},
            {"Name": "Security Deposit", "Score": 0.1605},
            {"Name": "Rent Deposit", "Score": 0.1577},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "28",
        "Classes": [
            {"Name": "Other", "Score": 0.2652},
            {"Name": "Security Deposit", "Score": 0.1605},
            {"Name": "Rent Deposit", "Score": 0.1577},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "29",
        "Classes": [
            {"Name": "Other", "Score": 0.2525},
            {"Name": "Security Deposit", "Score": 0.1726},
            {"Name": "Rent Deposit", "Score": 0.1569},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "30",
        "Classes": [
            {"Name": "Other", "Score": 0.2618},
            {"Name": "Guests Prohibited", "Score": 0.2168},
            {"Name": "Security Deposit", "Score": 0.1671},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "31",
        "Classes": [
            {"Name": "Other", "Score": 0.5168},
            {"Name": "Security Deposit", "Score": 0.1117},
            {"Name": "Guests Prohibited", "Score": 0.0969},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "32",
        "Classes": [
            {"Name": "Other", "Score": 0.8232},
            {"Name": "Security Deposit", "Score": 0.0646},
            {"Name": "Key Deposit", "Score": 0.0298},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "33",
        "Classes": [
            {"Name": "Security Deposit", "Score": 0.2177},
            {"Name": "Other", "Score": 0.212},
            {"Name": "Key Deposit", "Score": 0.1617},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "34",
        "Classes": [
            {"Name": "Other", "Score": 0.7083},
            {"Name": "Rent Deposit", "Score": 0.0931},
            {"Name": "Guests Prohibited", "Score": 0.0517},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "35",
        "Classes": [
            {"Name": "Other", "Score": 0.7386},
            {"Name": "Security Deposit", "Score": 0.0792},
            {"Name": "Rent Deposit", "Score": 0.0701},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "36",
        "Classes": [
            {"Name": "Pets Prohibited", "Score": 0.9486},
            {"Name": "Other", "Score": 0.0404},
            {"Name": "Guests Prohibited", "Score": 0.0047},
        ],
    },
    {
        "File": "e0eeacc0-9160-4791-a2a4-1eabe75695f2.txt",
        "Line": "37",
        "Classes": [
            {"Name": "Guests Prohibited", "Score": 0.99},
            {"Name": "Other", "Score": 0.0087},
            {"Name": "Rent Deposit", "Score": 0.0004},
        ],
    },
]
