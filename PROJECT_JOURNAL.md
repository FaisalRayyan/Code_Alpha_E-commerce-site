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