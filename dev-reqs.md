

________________________________________
📄 A1 WAVE Dashboard — Requirements Document
Ride macro waves. Exit before they break.
________________________________________
1. Project Overview
Build a web based dashboard for the A1 WAVE tactical momentum strategy.
The dashboard should display:
•	Theme level macro conditions
•	Green/Yellow/Red classification of positions
•	Velocity, trend, volume, catalyst status
•	Weekly rotation plan
•	Notes and decision fields
The dashboard must be interactive, auto updating, and data driven using free public data sources.
The dashboard can be built using Streamlit (preferred for speed) or HTML/NodeJS (if needed).
________________________________________
2. Tech Stack Requirements
Option A — Streamlit (Preferred)
•	Python 3.10+
•	Streamlit
•	yfinance (free Yahoo Finance API wrapper)
•	Requests (for news APIs)
•	Plotly or Matplotlib (optional for charts)
Option B — HTML/NodeJS
•	NodeJS + Express
•	Free finance APIs (Yahoo Finance unofficial endpoints)
•	Chart.js for visualizations
•	TailwindCSS or Bootstrap for layout
Either option must support:
•	Auto-refreshing data
•	Clean UI layout
•	Mobile-friendly design
________________________________________
3. Data Sources (Free)
The dashboard must use free, publicly accessible data sources:
Price, Volume, Trend Data
•	Yahoo Finance (via yfinance or direct API calls) 
o	Price
o	Volume
o	Moving averages
o	Relative strength vs SPY
o	1 month and 3 month returns
News / Catalyst Data
•	NewsAPI (free tier)
•	Google News RSS
•	Yahoo Finance news endpoints
Sector / Macro Data
•	SPY, QQQ, DIA (market trend)
•	Sector ETFs (XAR, ITA, UFO, IYZ)
•	Treasury yields (Yahoo Finance: ^TNX)
•	VIX (Yahoo Finance: ^VIX)
________________________________________
4. Dashboard Layout Requirements
The dashboard must contain the following sections:
________________________________________
Section 1 — Theme Level Panel (Top of Dashboard)
Fields:
•	Theme Name (e.g., “Space Economy Momentum”)
•	Macro Status (Risk On / Neutral / Risk Off)
•	Sector Strength (Strong / Moderate / Weak)
•	ETF Trend (Above / At / Below 20 day MA)
•	Narrative Status (Strengthening / Stable / Weakening)
•	Decision (Maintain Wave / Reduce Exposure / Prepare Exit)
Logic:
•	Macro Status determined by SPY trend + VIX level
•	Sector Strength determined by sector ETF performance
•	Narrative Status determined by news sentiment scoring
________________________________________
Section 2 — Green / Yellow / Red Panels
Three separate panels:
________________________________________
🟢 GREEN — Leaders (Add / Hold Full Weight)
Columns:
•	Ticker
•	Velocity Score
•	Trend Structure
•	Volume Profile
•	Catalyst Status
•	Action
•	Notes
Logic:
•	Velocity Score = strong 1 month + 3 month returns
•	Trend Structure = price above 20/50 day MA
•	Volume Profile = up volume > down volume
•	Catalyst Status = positive news sentiment
________________________________________
🟡 YELLOW — Slowing (Trim / Tighten Stops)
Columns:
•	Ticker
•	Velocity Score
•	Trend Structure
•	Volume Profile
•	Catalyst Status
•	Action
•	Notes
Logic:
•	Velocity Score = flattening returns
•	Trend Structure = testing 20 day MA
•	Volume Profile = mixed
•	Catalyst Status = neutral news sentiment
________________________________________
🔴 RED — Breaking (Exit / Rotate)
Columns:
•	Ticker
•	Velocity Score
•	Trend Structure
•	Volume Profile
•	Catalyst Status
•	Action
•	Notes
Logic:
•	Velocity Score = negative returns
•	Trend Structure = below 50 day MA
•	Volume Profile = distribution
•	Catalyst Status = negative news sentiment
________________________________________
Section 3 — Weekly Rotation Panel
Columns:
•	Add
•	Trim
•	Exit
•	Rotate
•	Rebalance
Logic:
•	Add = Green names with pullback opportunities
•	Trim = Yellow names with weakening velocity
•	Exit = Red names
•	Rotate = Move capital from Red → Green
•	Rebalance = Adjust Tier 1/2/3 weights
________________________________________
Section 4 — Notes & Journal Panel
Fields:
•	“Why I’m still in this wave”
•	“What would make me exit”
•	“Next week’s plan”
Requirements:
•	Editable text fields
•	Auto-save to local storage or JSON file
________________________________________
5. Backend Logic Requirements
Velocity Score Calculation
•	Compute 1 month return
•	Compute 3 month return
•	Compute slope of 20 day moving average
•	Combine into a score (Strong / Moderate / Weak)
Trend Structure
•	Above 20 day MA → Uptrend
•	Above 50 day MA → Strong uptrend
•	Below 50 day MA → Breakdown
Volume Profile
•	Compare average up volume vs down volume over 10 days
Catalyst Status
•	Use news sentiment scoring: 
o	Positive → Active
o	Neutral → Stable
o	Negative → Fading
Classification Logic
•	If velocity strong + trend strong → GREEN
•	If velocity slowing + trend flattening → YELLOW
•	If velocity negative + trend broken → RED
________________________________________
6. User Interaction Requirements
•	Dropdown to select theme (e.g., Space, AI, Defense)
•	Editable tickers list
•	Editable notes
•	Buttons: 
o	Refresh Data
o	Export Dashboard (JSON)
o	Reset Notes
________________________________________
7. UI/UX Requirements
•	Clean, modern layout
•	Color-coded sections (Green/Yellow/Red)
•	Responsive design
•	Minimal clutter
•	Clear typography
•	Optional dark mode
________________________________________
8. Deployment Requirements
•	Must run locally or via Streamlit Cloud / Vercel / Netlify
•	No paid APIs
•	No authentication required
•	Must load within 3–5 seconds
________________________________________
9. Deliverables
•	Fully functional dashboard
•	Source code (Python or NodeJS)
•	README with setup instructions
•	Config file for tickers and themes
•	Optional: Dockerfile
________________________________________
________________________________________
🌊 A1 WAVE Dashboard — UI Mockup (Text Wireframe)
Ride macro waves. Exit before they break.
Below is the full layout exactly as it should appear on screen.
________________________________________
┌───────────────────────────────────────────────────────────────┐
│                        A1 WAVE DASHBOARD                       │
│                Ride macro waves. Exit before they break.       │
└───────────────────────────────────────────────────────────────┘


=================================================================
SECTION 1 — THEME LEVEL PANEL (TOP)
=================================================================

┌───────────────────────────────────────────────────────────────┐
│ THEME: Space Economy Momentum                                  │
│                                                                 │
│ MACRO STATUS:   [ Risk On / Neutral / Risk Off ]               │
│ SECTOR STRENGTH: [ Strong / Moderate / Weak ]                  │
│ ETF TREND:       [ Above / At / Below 20 day MA ]              │
│ NARRATIVE:       [ Strengthening / Stable / Weakening ]        │
│                                                                 │
│ DECISION:        [ Maintain Wave / Reduce Exposure / Exit ]    │
└───────────────────────────────────────────────────────────────┘


=================================================================
SECTION 2 — POSITION CLASSIFICATION PANELS
=================================================================

===========================
🟢 GREEN — LEADERS
(Add / Hold Full Weight)
===========================

┌───────────────────────────────────────────────────────────────┐
│ Ticker | Velocity | Trend | Volume | Catalyst | Action | Notes │
├───────────────────────────────────────────────────────────────┤
│ RKLB   | Strong   | HH/HL | Accum. | Active   | Add    | ...   │
│ RDW    | Strong   | HH/HL | Accum. | Active   | Hold   | ...   │
└───────────────────────────────────────────────────────────────┘


===========================
🟡 YELLOW — SLOWING
(Trim / Tighten Stops)
===========================

┌───────────────────────────────────────────────────────────────┐
│ Ticker | Velocity | Trend | Volume | Catalyst | Action | Notes │
├───────────────────────────────────────────────────────────────┤
│ PL     | Slowing  | Flat  | Mixed  | Neutral  | Tighten | ...  │
│ BKSY   | Moderate | Test  | Mixed  | Neutral  | Trim    | ...  │
└───────────────────────────────────────────────────────────────┘


===========================
🔴 RED — BREAKING
(Exit / Rotate)
===========================

┌───────────────────────────────────────────────────────────────┐
│ Ticker | Velocity | Trend | Volume | Catalyst | Action | Notes │
├───────────────────────────────────────────────────────────────┤
│ SPIR   | Weak     | Break | Dist.  | Negative | Exit   | ...   │
│ SATL   | Weak     | LHL   | Dist.  | Negative | Exit   | ...   │
└───────────────────────────────────────────────────────────────┘


=================================================================
SECTION 3 — WEEKLY ROTATION PANEL
=================================================================

┌───────────────────────────────────────────────────────────────┐
│ ADD:      [ List tickers to add on dips ]                      │
│ TRIM:     [ List tickers to trim ]                             │
│ EXIT:     [ List tickers to exit ]                             │
│ ROTATE:   [ From → To ]                                        │
│ REBALANCE:[ Tier 1 / Tier 2 / Tier 3 adjustments ]             │
└───────────────────────────────────────────────────────────────┘


=================================================================
SECTION 4 — NOTES & JOURNAL PANEL
=================================================================

┌───────────────────────────────────────────────────────────────┐
│ WHY I’M STILL IN THIS WAVE:                                    │
│ [ Free text box ]                                              │
│                                                                 │
│ WHAT WOULD MAKE ME EXIT:                                       │
│ [ Free text box ]                                              │
│                                                                 │
│ NEXT WEEK’S PLAN:                                              │
│ [ Free text box ]                                              │
└───────────────────────────────────────────────────────────────┘


=================================================================
FOOTER
=================================================================

┌───────────────────────────────────────────────────────────────┐
│ Buttons: [ Refresh Data ] [ Export JSON ] [ Reset Notes ]      │
└───────────────────────────────────────────────────────────────┘
________________________________________
🎨 Design Notes for Developers
Layout
•	Use a three panel horizontal layout for Green / Yellow / Red on desktop
•	Collapse to vertical stacking on mobile
•	Theme panel always stays at the top
•	Notes panel always at the bottom
Colors
•	Green panel: #0FA958
•	Yellow panel: #F2C94C
•	Red panel: #EB5757
•	Theme panel: neutral slate or dark gray
Typography
•	Header: bold, large
•	Section titles: medium bold
•	Table text: regular, clean
Interactivity
•	Each row should be clickable to expand notes
•	Notes auto save locally
•	Refresh button triggers data reload

