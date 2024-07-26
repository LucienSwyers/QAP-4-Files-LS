// Define the MotelCustomer object
const MotelCustomer = {
    // Customer attributes
    Name: "Lucien Swyers",
    BirthDate: new Date(1985, 4, 15), // May 15, 1985
    Gender: "Male",
    RoomPreferences: ["Non-smoking", "King bed", "Ocean view"],
    PaymentMethod: "Credit Card",
    MailingAddress: {
        Street: "123 Maple Street",
        City: "Springfield",
        State: "IL",
        ZipCode: "62704",
        Country: "USA"
    },
    PhoneNumber: "555-1234",
    CheckIn: new Date(2023, 6, 15), // July 15, 2023
    CheckOut: new Date(2023, 6, 20), // July 20, 2023

    // Method to calculate age
    GetAge: function() {
        const Today = new Date();
        let Age = Today.getFullYear() - this.BirthDate.getFullYear();
        const MonthDiff = Today.getMonth() - this.BirthDate.getMonth();
        if (MonthDiff < 0 || (MonthDiff === 0 && Today.getDate() < this.BirthDate.getDate())) {
            Age--;
        }
        return Age;
    },

    // Method to calculate duration of stay
    GetStayDuration: function() {
        const TimeDiff = this.CheckOut.getTime() - this.CheckIn.getTime();
        const DaysDiff = TimeDiff / (1000 * 3600 * 24);
        return DaysDiff;
    },

    // Method to generate customer description
    GetCustomerDescription: function() {
        return `
            <p><strong>Name:</strong> ${this.Name}</p>
            <p><strong>Age:</strong> ${this.GetAge()}</p>
            <p><strong>Gender:</strong> ${this.Gender}</p>
            <p><strong>Room Preferences:</strong> ${this.RoomPreferences.join(", ")}</p>
            <p><strong>Payment Method:</strong> ${this.PaymentMethod}</p>
            <p><strong>Mailing Address:</strong></p>
            <p>${this.MailingAddress.Street}</p>
            <p>${this.MailingAddress.City}, ${this.MailingAddress.State} ${this.MailingAddress.ZipCode}, ${this.MailingAddress.Country}</p>
            <p><strong>Phone Number:</strong> ${this.PhoneNumber}</p>
            <p><strong>Check-In Date:</strong> ${this.CheckIn.toDateString()}</p>
            <p><strong>Check-Out Date:</strong> ${this.CheckOut.toDateString()}</p>
            <p><strong>Duration of Stay:</strong> ${this.GetStayDuration()} nights</p>
        `;
    }
};

// Display the customer information in the HTML
document.addEventListener("DOMContentLoaded", () => {
    const CustomerInfoDiv = document.getElementById("customerInfo");
    CustomerInfoDiv.innerHTML = MotelCustomer.GetCustomerDescription();
});
