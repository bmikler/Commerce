
# Commerce
### eBay-like e-commerce auction site that allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”.
#### Application created during CS50 web programming course.

# [Video presentation](https://www.youtube.com/watch?v=jyVg_qOEthw)


## Specification

* Create Listing: Users can visit a page to create a new listing. They are able to specify a title for the listing, a text-based description, and what the starting bid should be. Users can also optionally provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).

* Active Listings Page: The default route of web application should let users view all of the currently active auction listings. For each active listing, this page display the title, description, current price, and photo (if one exists for the listing).

* Listing Page: Clicking on a listing take users to a page specific to that listing. On that page, users are able to view all details about the listing, including the current price for the listing.

* If the user is signed in, the user can add the item to their “Watchlist.” If the item is already on the watchlist, the user can remove it.

* If the user is signed in, the user can bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the error message will appear.

* If the user is signed in and is the one who created the listing, the user have ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.

* Users who are signed in can add comments to the listing page. The listing page display all comments that have been made on the listing.

* Watchlist: Users who are signed in can visit a Watchlist page, which display all of the listings that a user has added to their watchlist. Clicking on any of those listings take the user to that listing’s page.

* Categories: Users can visit a page that displays a list of all listing categories. Clicking on the name of any category take the user to a page that displays all of the active listings in that category.