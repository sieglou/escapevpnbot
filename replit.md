# replit.md

## Overview

YouVPN is a Telegram bot service for VPN subscriptions featuring paid subscriptions, referral system, and Telegram Payments integration. The bot is built with Python using the aiogram framework and Supabase as the backend database. It provides users with subscription management, VPN connection instructions, referral rewards, and payment processing through Telegram's native payment system.

## System Architecture

### Backend Architecture
- **Framework**: Python 3.11+ with aiogram 3.x for Telegram bot functionality
- **Database**: Supabase (PostgreSQL cloud service) for user data, subscriptions, payments, and referral tracking
- **Payment Processing**: Telegram Payments API for handling subscription purchases
- **State Management**: aiogram's FSM (Finite State Machine) with MemoryStorage for user interaction flows

### Bot Structure
- **Modular Router System**: Separate handlers for different bot functions (start, payments, menu, referral)
- **Configuration Management**: Centralized config system using environment variables
- **Database Models**: Separate model files for users, subscriptions, and payments
- **Utility Functions**: Helper modules for database operations, notifications, and formatting

## Key Components

### 1. Core Bot Components
- `bot.py`: Main entry point with bot initialization and router registration
- `config.py`: Configuration management with environment variables validation
- `handlers/`: Modular command and callback handlers
- `models/`: Database interaction layer for different entities

### 2. User Management
- User registration and authentication via Telegram chat_id
- Profile management with Telegram user data synchronization
- Activity tracking and user state management

### 3. Subscription System
- Multiple subscription tiers (1, 2, 3, 6, 12 months)
- Subscription activation and renewal
- Expiration tracking and notifications
- VPN connection instructions delivery
- Integrated plan selection within VPN connection flow

### 4. Payment Processing
- Telegram Payments integration with RUB currency
- Payment record creation and tracking
- Automatic subscription activation upon successful payment
- Payment failure handling

### 5. Referral System
- Unique referral link generation for each user
- Reward tracking (100₽ per successful referral)
- Referral statistics and balance management
- Automatic reward distribution

### 6. Notification System
- Payment success notifications
- Subscription expiration warnings
- Referral reward notifications
- Scheduled notification tasks

## Data Flow

### User Registration Flow
1. User sends `/start` command
2. Bot creates/updates user record in Supabase
3. Bot retrieves subscription status
4. Bot displays personalized main menu

### Payment Flow
1. User selects subscription plan
2. Bot creates Telegram invoice
3. User completes payment through Telegram
4. Bot processes successful payment callback
5. Bot creates payment record and activates subscription
6. Bot sends confirmation notification

### Referral Flow
1. User requests referral link
2. Bot generates unique referral URL
3. Referred user joins via link
4. Bot tracks referral relationship
5. Upon referred user's first payment, referrer receives reward

## External Dependencies

### Required Services
- **Telegram Bot API**: Core bot functionality and payments
- **Supabase**: PostgreSQL database with real-time capabilities
- **Python Packages**:
  - `aiogram`: Telegram bot framework
  - `supabase`: Database client
  - `python-dotenv`: Environment variable management

### Environment Variables
- `BOT_TOKEN`: Telegram bot token from BotFather
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_KEY`: Supabase anonymous key
- `PAYMENT_TOKEN`: Telegram payment provider token
- `WEBSITE_URL`: Company website URL
- `SUPPORT_USERNAME`: Support contact username

## Deployment Strategy

### Replit Deployment
- **Runtime**: Python 3.11 with Nix package management
- **Dependencies**: Managed via pyproject.toml and automated installation
- **Configuration**: Environment variables stored in Replit Secrets
- **Execution**: Automated workflow for dependency installation and bot startup

### Database Schema
The application uses Supabase with the following main tables:
- `users`: User profiles and referral data
- `subscriptions`: Active and historical subscriptions
- `payments`: Payment transaction records
- `referrals`: Referral relationship tracking

### Scaling Considerations
- Memory-based state storage suitable for moderate user loads
- Supabase handles database scaling automatically
- Bot can be easily migrated to production environments

## Changelog

```
Changelog:
- June 16, 2025. Initial setup
- June 16, 2025. Added Telegram Stars payment support as alternative to traditional payments
- June 17, 2025. Migration from Replit Agent to standard Replit environment completed
- June 17, 2025. Updated VPN connection flow with integrated subscription plan selection
- June 17, 2025. Implemented new pricing structure (125-1300 Stars) with 2-month plan addition
- June 17, 2025. Simplified UI design for better user experience
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```