-- Keep a log of any SQL queries you execute as you solve the mystery.
-- 1. Identify the crime scene id based on year, month, day, street and additional information of the duck. The crime took place at 10:15am.
SELECT id, description
    FROM crime_scene_reports
        WHERE year = 2021 AND month = 7 AND day = 28
        AND description LIKE "%duck%";

-- 2. The description talks about interviews where the bakery is mentioned and ocurred on the same day or after.
SELECT *
    FROM interviews
        WHERE transcript LIKE "%bakery%"
        AND year = 2021 AND month >= 7 AND day >= 28;

-- We got some information from the interviews:
-- a) The thef have a car and within the next ten minutes of the theft he left the parking lot.
-- b) On the same day of the theft, the thief went to the ATM on Leggett Street.
-- c) The accomplice bought a fight ticket for the earliest flight out of Fiftyville on the next day.

-- 3. The list of license_plates that complies with the information in letter a):
SELECT *
    FROM bakery_security_logs
    WHERE activity = "exit"
        AND year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25;

-- 4. The list of people with the license_plates identified

SELECT people.name, people.license_plate, people.id
    FROM people
    JOIN bakery_security_logs AS bsl ON people.license_plate = bsl.license_plate
    WHERE bsl.activity = "exit"
    AND bsl.year = 2021 AND bsl.month = 7 AND bsl.day = 28 AND bsl.hour = 10 AND bsl.minute >= 15 AND bsl.minute <= 25;

-- 5. The list of account_numbers that complies with the information in letter b):
SELECT *
    FROM atm_transactions
    WHERE atm_location = "Leggett Street" AND transaction_type = "withdraw"
    AND year = 2021 AND month = 7 AND day = 28;

-- 6. The list of people that made a transaction on the Leggett Street ATM the same day of the robbery

SELECT people.name, bank_accounts.account_number, people.id
    FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id
    WHERE account_number IN (SELECT account_number
        FROM atm_transactions
        WHERE atm_location = "Leggett Street" AND transaction_type = "withdraw"
        AND year = 2021 AND month = 7 AND day = 28);

-- 7. The flight with the earliest flight for the next date, according to the information in letter c) and also to know the city:
SELECT id  FROM
    (SELECT flights.id, MIN(hour)
        FROM flights
        JOIN airports ON flights.origin_airport_id = airports.id
        WHERE airports.full_name LIKE "%Fiftyville%"
        AND year = 2021 AND month = 7 AND day = 29);

-- 8. The passengers from the selected flight:
SELECT id, name FROM people
    WHERE passport_number IN
        (SELECT passport_number FROM
            (SELECT * FROM passengers
                WHERE flight_id IN (SELECT id FROM
                    (SELECT flights.id, MIN(hour)
                        FROM flights
                        JOIN airports ON flights.origin_airport_id = airports.id
                        WHERE airports.full_name LIKE "%Fiftyville%"
                        AND year = 2021 AND month = 7 AND day = 29))));

-- 9. Look for the caller names:
SELECT * FROM people JOIN phone_calls AS pc ON people.phone_number = pc.caller
    WHERE pc.year = 2021 AND pc.month = 7 AND pc.day = 28;

-- 10. Merge the names id and names of information a) and b) and the flight from c):

SELECT name, id
    FROM

        (SELECT name, id
            FROM (SELECT people.name, bank_accounts.account_number, people.id
                FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id
                WHERE account_number IN (SELECT account_number
                    FROM atm_transactions
                    WHERE atm_location = "Leggett Street" AND transaction_type = "withdraw"
                    AND year = 2021 AND month = 7 AND day = 28))

                    WHERE id IN (SELECT people.id
                            FROM people
                            JOIN bakery_security_logs AS bsl ON people.license_plate = bsl.license_plate
                            WHERE bsl.activity = "exit"
                            AND bsl.year = 2021 AND bsl.month = 7 AND bsl.day = 28 AND bsl.hour = 10 AND bsl.minute >= 15 AND bsl.minute <= 25))

                            WHERE id IN
                                (SELECT id FROM people
                                    WHERE passport_number IN
                                        (SELECT passport_number FROM
                                            (SELECT * FROM passengers
                                                WHERE flight_id IN (SELECT id FROM
                                                    (SELECT flights.id, MIN(hour)
                                                        FROM flights
                                                        JOIN airports ON flights.origin_airport_id = airports.id
                                                        WHERE airports.full_name LIKE "%Fiftyville%"
                                                        AND year = 2021 AND month = 7 AND day = 29)))));

-- 11. We look for the destination city:
SELECT city FROM airports WHERE id IN
        (SELECT destination_airport_id FROM
            (SELECT flights.id, flights.destination_airport_id, MIN(hour)
                FROM flights
                JOIN airports ON flights.origin_airport_id = airports.id
                WHERE airports.full_name LIKE "%Fiftyville%"
                AND year = 2021 AND month = 7 AND day = 29));

-- 12. Then we see the phone calls and we deduct Bruce with id 686048, the only one with a caller phone call, made the theft.

-- 13. Get the phone_numbers of receivers of Bruce calls of less than a minute:
SELECT name FROM people
    WHERE phone_number IN
        (SELECT pc.receiver FROM people JOIN phone_calls AS pc ON people.phone_number = pc.caller
            WHERE pc.year = 2021 AND pc.month = 7 AND pc.day = 28 AND people.id = 686048 AND pc.duration < 60);

