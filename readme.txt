# Small Business Site - The Lawn Duck Crew
#### Video Demo: URL
#### Description:
My project is a website for a lawn & garden maintenance business. It comes complete with a summary of information on its services and includes a Contact Us form for customer enquiries.
Upon submission, the contact form sends the enquiry to the Flask backend, where it is processed and added to an SQLite database.
The completion of the contact us form also triggers an email to the Business Owner (BO), which outlines the details of the customers enquiry.
Each day at 6pm the BO receives a scheduled email which outlines how many new enquiries were received that day.
The BO is able to log in to the site and see all the enquiries in one place.
The BO is able to mark enquiries as 'Contacted' from their default 'Not Contacted' status.
The BO is also able to add a short note to each enquiry, which is sent to and stored in the database.

#### Features
- Mobile optimisation; depending on the width of the devices browser the modules will collapse into a single column, and the size of images will also adjust, which Bootstrap helped with.
- Device responsive dark mode based on the code in [1].
- Specialised drop down that focuses on optimised UX ("When is the work required?")
- Simple layout and navigation to suit users of all ages
- Carousels used for 'before & after' photos, thanks to Bootstrap.
- Carousels used for 'about us' team photos, thanks to Bootstrap.
- Accordions used to tidy up the 'Services' page and avoid too much text showing at one time, thanks to Bootstrap.
- Contact us form adapted for this specific use case and includes various client side validations to maintain data integrity such as not submitting the form if certain fields are blank, limiting character length, or specifying character length.
- Contact us form flashes thank you message
- Contact us form triggers email to BO with details of the customers enquiry, which uses Flask-Mail.
- Daily Scheduled email that summarises how many enquiries were received for the day, how urgent each enquiries is, and a total of how many enquiries have still not been contacted. This uses Flask-Mail and APScheduler.
- Staff logins can only be created by a python script run in the backend
- Staff login can only be navigated to via "/login" route, this is avoid bad actors brute forcing their way into the site
- Staff login allows password changes
- Staff view enables BO to see all enquiries in order of Newest to Oldest.
- Staff view has integrated pagination which shows 5 enquiries per page, with an undefined limit of pages. [2][8]
- Staff view allows the user to mark enquiries as 'Contacted' (from 'Not Contacted') via a button that changes colour from grey to green when pressed, as well as updating the Status of the enquiry in the back-end. [3]
- User is able to press this button again without reloading the page in case it was pressed by accident.
- Enquiries that have Status == 'Not Contacted' show how old the enquiry is in Days and Hours, in order to give the BO a clear idea of how old an enquiry is.[4][9]
- Staff view allows the user to add a note to enquiries via a text box.[5]
- User is able to save the note via a button, which sends the note to the back-end via JavaScript, and also updates what the user can see on the front-end.[6][7]


#### Usage
Using the site is fairly intuitive if you're a customer. User intuition was something that I tried to keep front of mind when designing the site and it's layout.
I also reduced my workload a bit by using a sitemap that reused certain blocks of code. For example the Contact Us form exists in three locations in the site. As a result, I refrained from putting any code in the second and third locations until I was satisfied that the code for the form was final.
This is also the case for the Before & After Carousel, Social Media Reviews, and to an extent the descriptions of the services the business provides.

From the point of view of a staff member or business owner, a short guide is provided below, though I still tried to make the site and intuitive as possible.
1. Access staff login by adding "/login" to the end of the site URL.
2. Username and password have been provided separately
3. If a password change is required this can be done once logged in
4. Press the 'Not Contacted' button order to mark an enquiry as 'Contacted'
5. If the button was pressed by accident, press it again to revert to the other status
6. To add a note, click on the text box, add the note then press 'Save'
7. Enquiries are in order of Newest to Oldest
8. Enquiries that have their Status as 'Not Contacted' will show the age of the enquiry, if this isn't working simply refresh the page
9. Each form submission will send a triggered email to the BO's email
10. The Daily summary will be send at 18:00 hours each day

#### Citations
1. Stefan Haack, "bootstrap-auto-dark-mode," https://github.com/shaack/bootstrap-auto-dark-mode
2. CS50 AI, "Provided guidance on implementing dynamic pagination with pages ranging from 1 to n," interaction on 31-08-2024.
3. CS50 AI, "Provided guidance on implementing dynamic buttons that display certain text and color based on 'Status' value," interaction on 09-09-2024.
4. CS50 AI, "Provided guidance on dynamically displaying age on an enquiry if status is not equal to 'Contacted'," interaction on 10-09-2024.
5. CS50 AI, "Provided guidance on implementing an editable note section for each enquiry," interaction on 10-09-2024.
6. ChatGPT, "Provided guidance on JavaScript for 'Status' button functionality," interaction on 09-09-2024.
7. ChatGPT, "Provided guidance on JavaScript for 'Notes' functionality," interaction on 10-09-2024.
8. CS50 AI, "Provided guidance on possible ways to set up pagination variables back to the rendered '/staff' webpage," interaction on 31-08-2024.
9. CS50 AI, "Provided guidance on how to perform the calculation for age on an enquiry," interaction on 10-09-2024.

#### Credits
For acknowledging contributions and tools:
- **Flask**: Used for the web framework.
- **Flask-Mail**: Used for sending emails to the business owner/manager.
- **Flask-Session**: Used for session management.
- **Werkzeug Security**: Used for password hashing and checking.
- **CS50 Library**: Used for SQL integration.
- **APScheduler**: Used for scheduling background tasks and scheduled emails.
- **datetime**: Used for date and time functions.
- **functools**: Used for utility functions like wraps.
- **Bootstrap**: Used for styling and front-end features such as button styling, cards, contact forms, font styles, general website layout, image carousels, mobile optimization, modals, modules, navigation bars, page spacing, social media buttons, and tables.

#### Acknowledgements
For expressing gratitude for support and guidance:
Week 9 Flask: Finace Problem Set to help with the set up of the site, user creation and password changes.

#### License
This project is licensed under the MIT License.
