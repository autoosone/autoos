-- ============================================
-- AUTO MARKETPLACE SUPABASE SCHEMA
-- Database: postgres
-- Project: fyqdlfdthkkslbwtsvmq
-- ============================================

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis"; -- For location-based features

-- ============================================
-- CORE TABLES
-- ============================================

-- 1. DEALERS TABLE
-- Stores information about car dealerships
CREATE TABLE IF NOT EXISTS dealers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    website VARCHAR(255),
    
    -- Address information
    address_street VARCHAR(255),
    address_city VARCHAR(100),
    address_state VARCHAR(50),
    address_zip VARCHAR(10),
    address_country VARCHAR(100) DEFAULT 'USA',
    
    -- Location for mapping
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    location GEOGRAPHY(POINT),
    
    -- Business details
    license_number VARCHAR(100),
    established_year INTEGER,
    description TEXT,
    logo_url VARCHAR(500),
    cover_image_url VARCHAR(500),
    
    -- Ratings and stats
    rating DECIMAL(2, 1) CHECK (rating >= 0 AND rating <= 5),
    total_reviews INTEGER DEFAULT 0,
    total_sales INTEGER DEFAULT 0,
    
    -- Operating hours (JSON format)
    operating_hours JSONB,
    
    -- Features and services
    services TEXT[], -- Array of services offered
    brands TEXT[], -- Array of brands sold
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    verified_at TIMESTAMP WITH TIME ZONE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. VEHICLES TABLE
-- Stores vehicle inventory
CREATE TABLE IF NOT EXISTS vehicles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dealer_id UUID REFERENCES dealers(id) ON DELETE CASCADE,
    
    -- Vehicle identification
    vin VARCHAR(17) UNIQUE,
    stock_number VARCHAR(50),
    
    -- Basic info
    year INTEGER NOT NULL CHECK (year >= 1900 AND year <= 2100),
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    trim VARCHAR(100),
    body_type VARCHAR(50), -- SUV, Sedan, Truck, etc.
    
    -- Specifications
    engine VARCHAR(100),
    transmission VARCHAR(50),
    drivetrain VARCHAR(20), -- FWD, RWD, AWD, 4WD
    fuel_type VARCHAR(50), -- Gasoline, Electric, Hybrid, Diesel
    
    -- Mileage and efficiency
    mileage INTEGER,
    mpg_city INTEGER,
    mpg_highway INTEGER,
    
    -- Colors
    exterior_color VARCHAR(50),
    interior_color VARCHAR(50),
    
    -- Pricing
    price DECIMAL(10, 2),
    msrp DECIMAL(10, 2),
    sale_price DECIMAL(10, 2),
    is_on_sale BOOLEAN DEFAULT false,
    
    -- Condition
    condition VARCHAR(20), -- New, Used, Certified
    certified_preowned BOOLEAN DEFAULT false,
    one_owner BOOLEAN DEFAULT false,
    accident_free BOOLEAN DEFAULT false,
    
    -- Features (stored as JSON array)
    features JSONB,
    
    -- Images
    primary_image_url VARCHAR(500),
    images JSONB, -- Array of image URLs
    
    -- Description
    description TEXT,
    dealer_notes TEXT,
    
    -- Availability
    status VARCHAR(20) DEFAULT 'available', -- available, pending, sold, hold
    is_featured BOOLEAN DEFAULT false,
    
    -- History
    carfax_url VARCHAR(500),
    autocheck_url VARCHAR(500),
    
    -- Timestamps
    listed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    sold_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. USERS TABLE
-- Stores customer information
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    auth_id UUID UNIQUE, -- Links to Supabase Auth
    
    -- Basic info
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    
    -- Profile
    avatar_url VARCHAR(500),
    bio TEXT,
    
    -- Location
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    
    -- Preferences (for recommendations)
    preferred_makes TEXT[],
    preferred_body_types TEXT[],
    budget_min DECIMAL(10, 2),
    budget_max DECIMAL(10, 2),
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    phone_verified BOOLEAN DEFAULT false,
    
    -- Timestamps
    last_login_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. LEADS TABLE
-- Stores customer inquiries and leads
CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    dealer_id UUID REFERENCES dealers(id) ON DELETE CASCADE,
    vehicle_id UUID REFERENCES vehicles(id) ON DELETE SET NULL,
    
    -- Contact info (if not registered user)
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    
    -- Lead details
    type VARCHAR(50), -- inquiry, test_drive, finance, trade_in
    message TEXT,
    preferred_contact_method VARCHAR(20), -- email, phone, text
    preferred_contact_time VARCHAR(50),
    
    -- Status tracking
    status VARCHAR(50) DEFAULT 'new', -- new, contacted, qualified, appointment, closed_won, closed_lost
    priority VARCHAR(20) DEFAULT 'medium', -- low, medium, high, urgent
    assigned_to VARCHAR(255), -- Dealer staff member
    
    -- Follow-up
    follow_up_date DATE,
    notes TEXT,
    
    -- Source tracking
    source VARCHAR(100), -- website, mobile, api, chat
    utm_source VARCHAR(255),
    utm_medium VARCHAR(255),
    utm_campaign VARCHAR(255),
    
    -- Timestamps
    contacted_at TIMESTAMP WITH TIME ZONE,
    qualified_at TIMESTAMP WITH TIME ZONE,
    closed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. APPOINTMENTS TABLE
-- Stores test drive and service appointments
CREATE TABLE IF NOT EXISTS appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    dealer_id UUID REFERENCES dealers(id) ON DELETE CASCADE,
    vehicle_id UUID REFERENCES vehicles(id) ON DELETE SET NULL,
    
    -- Appointment details
    type VARCHAR(50), -- test_drive, service, appraisal, financing
    scheduled_date DATE NOT NULL,
    scheduled_time TIME NOT NULL,
    duration_minutes INTEGER DEFAULT 60,
    
    -- Status
    status VARCHAR(50) DEFAULT 'scheduled', -- scheduled, confirmed, completed, cancelled, no_show
    
    -- Notes
    customer_notes TEXT,
    dealer_notes TEXT,
    
    -- Confirmation
    confirmation_code VARCHAR(50),
    confirmed_at TIMESTAMP WITH TIME ZONE,
    reminder_sent_at TIMESTAMP WITH TIME ZONE,
    
    -- Timestamps
    completed_at TIMESTAMP WITH TIME ZONE,
    cancelled_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. SAVED_SEARCHES TABLE
-- Stores user's saved search criteria
CREATE TABLE IF NOT EXISTS saved_searches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    
    -- Search criteria
    name VARCHAR(255),
    criteria JSONB NOT NULL, -- Stores all search parameters
    
    -- Notifications
    email_alerts BOOLEAN DEFAULT false,
    push_alerts BOOLEAN DEFAULT false,
    alert_frequency VARCHAR(20), -- daily, weekly, instant
    
    -- Activity
    last_alerted_at TIMESTAMP WITH TIME ZONE,
    search_count INTEGER DEFAULT 0,
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. SAVED_VEHICLES TABLE
-- Stores user's favorited vehicles
CREATE TABLE IF NOT EXISTS saved_vehicles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    vehicle_id UUID REFERENCES vehicles(id) ON DELETE CASCADE,
    
    -- Notes
    notes TEXT,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Ensure unique combination
    UNIQUE(user_id, vehicle_id)
);

-- 8. REVIEWS TABLE
-- Stores dealer reviews
CREATE TABLE IF NOT EXISTS reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dealer_id UUID REFERENCES dealers(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    vehicle_id UUID REFERENCES vehicles(id) ON DELETE SET NULL,
    
    -- Review content
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(255),
    content TEXT,
    
    -- Categories
    sales_experience INTEGER CHECK (sales_experience >= 1 AND sales_experience <= 5),
    financing_experience INTEGER CHECK (financing_experience >= 1 AND financing_experience <= 5),
    service_experience INTEGER CHECK (service_experience >= 1 AND service_experience <= 5),
    
    -- Verification
    is_verified_purchase BOOLEAN DEFAULT false,
    
    -- Status
    is_published BOOLEAN DEFAULT true,
    is_flagged BOOLEAN DEFAULT false,
    
    -- Response
    dealer_response TEXT,
    dealer_response_at TIMESTAMP WITH TIME ZONE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 9. FINANCING_QUOTES TABLE
-- Stores financing quotes and pre-approvals
CREATE TABLE IF NOT EXISTS financing_quotes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    vehicle_id UUID REFERENCES vehicles(id) ON DELETE SET NULL,
    
    -- Loan details
    vehicle_price DECIMAL(10, 2),
    down_payment DECIMAL(10, 2),
    loan_amount DECIMAL(10, 2),
    term_months INTEGER,
    interest_rate DECIMAL(5, 3),
    monthly_payment DECIMAL(10, 2),
    
    -- Applicant info
    credit_score_range VARCHAR(50),
    annual_income DECIMAL(10, 2),
    
    -- Quote details
    lender_name VARCHAR(255),
    quote_reference VARCHAR(100),
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending', -- pending, approved, declined, expired
    expires_at TIMESTAMP WITH TIME ZONE,
    
    -- Timestamps
    approved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 10. TRADE_IN_VALUATIONS TABLE
-- Stores trade-in vehicle valuations
CREATE TABLE IF NOT EXISTS trade_in_valuations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    dealer_id UUID REFERENCES dealers(id) ON DELETE SET NULL,
    
    -- Vehicle info
    vin VARCHAR(17),
    year INTEGER,
    make VARCHAR(100),
    model VARCHAR(100),
    trim VARCHAR(100),
    mileage INTEGER,
    condition VARCHAR(50),
    
    -- Valuation
    estimated_value DECIMAL(10, 2),
    offer_amount DECIMAL(10, 2),
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending', -- pending, offered, accepted, declined, expired
    expires_at TIMESTAMP WITH TIME ZONE,
    
    -- Notes
    notes TEXT,
    
    -- Timestamps
    offered_at TIMESTAMP WITH TIME ZONE,
    accepted_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

-- Dealers indexes
CREATE INDEX idx_dealers_location ON dealers USING GIST(location);
CREATE INDEX idx_dealers_is_active ON dealers(is_active);
CREATE INDEX idx_dealers_rating ON dealers(rating);

-- Vehicles indexes
CREATE INDEX idx_vehicles_dealer_id ON vehicles(dealer_id);
CREATE INDEX idx_vehicles_make_model ON vehicles(make, model);
CREATE INDEX idx_vehicles_year ON vehicles(year);
CREATE INDEX idx_vehicles_price ON vehicles(price);
CREATE INDEX idx_vehicles_status ON vehicles(status);
CREATE INDEX idx_vehicles_condition ON vehicles(condition);
CREATE INDEX idx_vehicles_body_type ON vehicles(body_type);
CREATE INDEX idx_vehicles_fuel_type ON vehicles(fuel_type);

-- Leads indexes
CREATE INDEX idx_leads_dealer_id ON leads(dealer_id);
CREATE INDEX idx_leads_user_id ON leads(user_id);
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_created_at ON leads(created_at);

-- Appointments indexes
CREATE INDEX idx_appointments_dealer_id ON appointments(dealer_id);
CREATE INDEX idx_appointments_user_id ON appointments(user_id);
CREATE INDEX idx_appointments_scheduled_date ON appointments(scheduled_date);
CREATE INDEX idx_appointments_status ON appointments(status);

-- Reviews indexes
CREATE INDEX idx_reviews_dealer_id ON reviews(dealer_id);
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);

-- ============================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================

-- Enable RLS on all tables
ALTER TABLE dealers ENABLE ROW LEVEL SECURITY;
ALTER TABLE vehicles ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE saved_searches ENABLE ROW LEVEL SECURITY;
ALTER TABLE saved_vehicles ENABLE ROW LEVEL SECURITY;
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE financing_quotes ENABLE ROW LEVEL SECURITY;
ALTER TABLE trade_in_valuations ENABLE ROW LEVEL SECURITY;

-- ============================================
-- POLICIES
-- ============================================

-- Public read access to dealers and vehicles
CREATE POLICY "Public can view active dealers" ON dealers
    FOR SELECT USING (is_active = true);

CREATE POLICY "Public can view available vehicles" ON vehicles
    FOR SELECT USING (status = 'available');

-- Users can view and update their own data
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid() = auth_id);

CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid() = auth_id);

-- Users can manage their own saved items
CREATE POLICY "Users can manage own saved searches" ON saved_searches
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own saved vehicles" ON saved_vehicles
    FOR ALL USING (auth.uid() = user_id);

-- Users can view their own leads and appointments
CREATE POLICY "Users can view own leads" ON leads
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can view own appointments" ON appointments
    FOR SELECT USING (auth.uid() = user_id);

-- Public can create leads (for non-authenticated inquiries)
CREATE POLICY "Public can create leads" ON leads
    FOR INSERT WITH CHECK (true);

-- Users can create and view their own reviews
CREATE POLICY "Users can create reviews" ON reviews
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Public can view published reviews" ON reviews
    FOR SELECT USING (is_published = true);

-- ============================================
-- FUNCTIONS AND TRIGGERS
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updated_at
CREATE TRIGGER update_dealers_updated_at BEFORE UPDATE ON dealers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_vehicles_updated_at BEFORE UPDATE ON vehicles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_leads_updated_at BEFORE UPDATE ON leads
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_appointments_updated_at BEFORE UPDATE ON appointments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to update dealer ratings
CREATE OR REPLACE FUNCTION update_dealer_rating()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE dealers
    SET rating = (
        SELECT AVG(rating)::DECIMAL(2,1)
        FROM reviews
        WHERE dealer_id = NEW.dealer_id AND is_published = true
    ),
    total_reviews = (
        SELECT COUNT(*)
        FROM reviews
        WHERE dealer_id = NEW.dealer_id AND is_published = true
    )
    WHERE id = NEW.dealer_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update dealer rating when review is added/updated
CREATE TRIGGER update_dealer_rating_trigger
AFTER INSERT OR UPDATE ON reviews
    FOR EACH ROW EXECUTE FUNCTION update_dealer_rating();

-- Function to generate location point from lat/lng
CREATE OR REPLACE FUNCTION update_location_from_coordinates()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.latitude IS NOT NULL AND NEW.longitude IS NOT NULL THEN
        NEW.location = ST_SetSRID(ST_MakePoint(NEW.longitude, NEW.latitude), 4326);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update location when coordinates change
CREATE TRIGGER update_dealer_location
BEFORE INSERT OR UPDATE ON dealers
    FOR EACH ROW EXECUTE FUNCTION update_location_from_coordinates();

-- ============================================
-- SEED DATA (Optional - Sample Denver Dealers)
-- ============================================

-- Insert sample dealers
INSERT INTO dealers (name, slug, email, phone, address_street, address_city, address_state, address_zip, latitude, longitude, rating, services, brands, is_active, is_verified)
VALUES 
    ('AutoMax Denver', 'automax-denver', 'info@automaxdenver.com', '303-555-0100', '123 Broadway St', 'Denver', 'CO', '80202', 39.7392, -104.9903, 4.8, ARRAY['Sales', 'Service', 'Financing'], ARRAY['Honda', 'Toyota', 'Mazda'], true, true),
    ('Premium Motors', 'premium-motors', 'sales@premiummotors.com', '303-555-0200', '456 Colfax Ave', 'Aurora', 'CO', '80010', 39.7294, -104.8319, 4.6, ARRAY['Sales', 'Leasing', 'Trade-In'], ARRAY['BMW', 'Mercedes', 'Audi'], true, true),
    ('City Auto Sales', 'city-auto-sales', 'contact@cityautosales.com', '303-555-0300', '789 Main St', 'Littleton', 'CO', '80120', 39.6133, -104.9500, 4.7, ARRAY['Sales', 'Financing', 'Warranty'], ARRAY['Ford', 'Chevrolet', 'GMC'], true, true);

-- ============================================
-- PERMISSIONS GRANT (for application user)
-- ============================================

-- Grant usage on schema
GRANT USAGE ON SCHEMA public TO anon, authenticated;

-- Grant permissions on tables
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO anon, authenticated;
