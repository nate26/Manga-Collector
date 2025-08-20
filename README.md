## TODO List

### Quality Checklist:

- [ ] authorization with edit mode and login features
- [ ] refresh token if server has been restarted or something goes stale with user token

### Epics:

- [x] <font color="gray"> ~~Collection Editor~~ </font>
- [x] <font color="gray"> ~~Authorization~~ </font>
- [x] <font color="gray"> ~~Series Viewer~~ </font>
- [x] <font color="gray"> ~~Browse Volume Sales~~ </font>
- [ ] [<font color="orange"> REQUIRED </font>] Admin Records Editor
- [ ] Admin Add Volumes
- [ ] Item Search
- [ ] User Lists (Wishlists, etc...)
- [ ] Series Editions
- [ ] [<font color="limegreen"> IN PROGRESS </font>] Browse Series

### One-Off Enhancements:

- [ ] [<font color="orange"> REQUIRED </font>] Error Handling on Data Fetching
- [ ] [<font color="orange"> REQUIRED </font>] Loading Wheel on Data Fetching and Filtering
- [ ] Stylized Scrollbar

### Bugfixes:

- None 😎

### Tech Debt:

- [ ] [<font color="orange"> REQUIRED </font>] Move Login to Elixir
- [ ] [<font color="orange"> REQUIRED </font>] Unit Testing
- [ ] Functional Testing
- [x] <font color="gray"> ~~Improve Filtering Performance~~ </font>
- [ ] [<font color="limegreen"> IN PROGRESS </font>] Display Grid for Volume Viewer
- [ ] [<font color="limegreen"> IN PROGRESS </font>] Moving Style to Tailwind
- [ ] Address Cover Images (performance, safety, cookies)
- [ ] Cleanup Interfaces with service

### Series Viewer:

- [x] <font color="gray"> ~~Fix Volume Image Display~~ </font>
- [ ] Add Volume Tags (Owned, Unowned, Sale, Read)
- [x] <font color="gray"> ~~Volume Details Window~~ </font>
- [x] <font color="gray"> ~~Lazy Load Volume Data~~ </font>
- [ ] Add Sale Data to Volume Details if Unowned
- [ ] Add Collection Data to Volume Details if Owned
- [x] <font color="gray"> ~~Create Series Page~~ </font>
- [ ] Link to Series Page

### Browse Volume Sales:

- [x] <font color="gray"> ~~Display Volumes With Sales~~ </font>
- [x] <font color="gray"> ~~Display Sale Price Tag~~ </font>
- [x] <font color="gray"> ~~Move Model Change to Service~~ </font>
- [ ] Provide Link To Store
- [x] <font color="gray"> ~~Volume Details Window~~ </font>
- [ ] [<font color="limegreen"> IN PROGRESS </font>] Display Link to Series Page
- [ ] [<font color="limegreen"> IN PROGRESS </font>] Enhance Filtering (series filters)
- [ ] Add to Purchase List
- [ ] Remove from Purchase List
- [ ] Display Current Cost in Purchase List
- [ ] Enable Disabling on Purchase List

### Browse Series:

- [x] <font color="gray"> ~~Display Series Suggestions~~ </font>
- [ ] Filter by owned series

### Editing:

- [ ] [<font color="orange"> REQUIRED </font>] Error Message on Save Fail
- [ ] Volume Bulk Editing

### Filtering:

- [ ] Enhanced Date Filter (ranges for since, before, between)
- [ ] Enhanced Tag Filter (inline, select autofill dropdown, add button)
- [x] <font color="gray"> ~~Enhanced Cost Filter (min, max, range)~~ </font>
- [x] <font color="gray"> ~~Autofill Filter~~ </font>
- [ ] Investigate Options for Other Filters on Data
