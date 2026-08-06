# ShopSphere Development Journal

## Project Overview

ShopSphere is a premium full-stack e-commerce website focused
on joggers and sneakers.

This project is being developed as part of my CodeAlpha
Full Stack Development internship.

## Day 1 — Project Foundation

**Date:** 3 August 2026

### Work Completed

- Created and cloned the GitHub repository
- Created a Python virtual environment
- Installed Django and Pillow
- Initialized the Django project
- Created separate Django applications:
  - Core
  - Products
  - Accounts
  - Cart
  - Orders
- Configured templates and static files
- Created the first Django-powered homepage
- Connected CSS and JavaScript
- Verified the frontend through the browser console
- Completed initial database migrations

### What I Learned

- How Python virtual environments work
- Difference between a Django project and Django applications
- How Django URL routing works
- How Django templates are rendered
- How static CSS and JavaScript files are connected
- Why virtual environment files should not be uploaded to GitHub

### Next Step

The next phase will focus on the database structure,
product categories, products, variants, images, and the
Django admin panel.

## Day 2 — Product Catalog and Admin Management

**Date:** 4 August 2026

### Work Completed

- Created category, product, product image, and product variant models
- Added pricing, discount, stock, SKU, and visibility fields
- Created database migrations
- Customized the Django administration panel
- Created an administrator account
- Added the first category and sample product
- Added size and color-based product variants
- Tested product image uploads
- Displayed database products dynamically on the shop page
- Created a dynamic product details page
- Added image gallery, size selection, color display, stock status, and quantity controls

### What I Learned

- How Django models create database tables
- How relationships connect categories, products, images, and variants
- How Django migrations update the database
- How Django Admin manages application data
- How database records are rendered inside Django templates
- How dynamic slug-based product URLs work
- How frontend JavaScript handles product selections and gallery interactions

### Next Step

The next phase will implement the real shopping cart backend,
session-based cart storage, stock validation, cart totals,
and cart management.
## Day 3 — Shopping Cart Backend

**Date:** 5 August 2026

### Work Completed

- Created Cart and CartItem database models
- Added separate carts for authenticated users and guest sessions
- Implemented product variant and stock validation
- Created a real Add to Cart backend
- Prevented duplicate variant rows inside the same cart
- Added quantity accumulation for existing cart items
- Customized cart monitoring in Django Admin
- Created a responsive customer-facing Cart page
- Added quantity increase and decrease controls
- Added remove-item functionality
- Calculated line totals, cart subtotal, and total item quantity
- Added a global live cart counter
- Verified separate authenticated and Incognito guest carts

### What I Learned

- How Django sessions identify anonymous visitors
- How authenticated and guest carts can be stored separately
- How database constraints prevent duplicate cart items
- How backend stock validation protects inventory
- How POST requests update and remove cart items
- How Django context processors provide cart data globally
- How cart totals can be calculated dynamically from database records

### Next Step

The next phase will focus on user authentication, registration,
login, customer profiles, and connecting guest carts with
authenticated customer accounts.
## Day 4 — Customer Authentication and Profile Management

**Date:** 6 August 2026

### Work Completed

- Created the CustomerProfile database model
- Added automatic profile creation for new users
- Created a secure customer registration system
- Added duplicate email and phone-number validation
- Implemented customer login and logout
- Added separate authenticated navigation states
- Implemented guest-cart merging after customer login
- Created a protected customer profile page
- Added profile and shipping-address editing
- Added dynamic cart information to the customer profile
- Implemented secure password changing
- Preserved the authenticated session after password updates
- Added password show and hide controls
- Tested old-password rejection and new-password login
- Improved navigation and authentication interface styling

### What I Learned

- How Django authentication securely stores passwords
- How login and logout sessions work
- How login-required views protect customer pages
- How guest carts can merge into customer carts
- How one-to-one profiles extend Django users
- How multiple forms can update related database records
- How Django password validation and session authentication work
- How password visibility controls improve user experience

### Next Step

The next phase will focus on checkout, shipping information,
order database models, order placement, stock deduction,
order history, and admin order-status management.