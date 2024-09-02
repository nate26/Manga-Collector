## TODO List

### Quality Checklist:
- [ ] authorization with edit mode and login features
- [ ] refresh token if server has been restarted or something goes stale with user token

### Epics:
- [x] <font color="gray"> ~~Collection Editor~~ </font>
- [x] <font color="gray"> ~~Authorization~~ </font>
- [ ] [<font color="limegreen"> IN PROGRESS </font>] Series Viewer
- [ ] [<font color="limegreen"> IN PROGRESS </font>] Browse Volume Sales
- [ ] [<font color="orange"> REQUIRED </font>] Admin Records Editor
- [ ] Admin Add Volumes
- [ ] Item Search
- [ ] User Lists (Wishlists, etc...)
- [ ] Series Editions
- [ ] Browse Series

### One-Off Enhancements:
- [ ] [<font color="orange"> REQUIRED </font>] Error Handling on Data Fetching
- [ ] [<font color="orange"> REQUIRED </font>] Loading Wheel on Data Fetching and Filtering
- [ ] Stylized Scrollbar

### Bugfixes:
- None 😎

### Tech Debt:
- [ ] [<font color="orange"> REQUIRED </font>] Unit Testing
- [ ] Functional Testing
- [ ] Improve Filtering Performance
- [ ] Display Grid for Volume Viewer
- [ ] Moving Style to Tailwind
- [ ] Add Batching on Get for Performance
- [ ] Address Cover Images (performance, safety, cookies)
- [ ] GQL Rate Limiting
- [ ] Cleanup Interfaces with GQL

### Series Viewer:
- [x] Fix Volume Image Display
- [ ] Lazy Load Volume Data
- [ ] Add Volume Tags (Owned, Unowned, Sale, Read)
- [ ] Volume Details Window
- [ ] Add Sale Data to Volume Details if Unowned
- [ ] Add Collection Data to Volume Details if Owned
- [ ] Create Series Page
- [ ] Link to Series Page

### Browse Volume Sales:
- [x] Display Volumes With Sales
- [x] Display Sale Price Tag
- [ ] Provide Link To Store
- [ ] Display Link to Series Page
- [ ] Add to Purchase List
- [ ] Remove from Purchase List
- [ ] Display Current Cost in Purchase List
- [ ] Enable Disabling on Purchase List
- [ ] Enhance Filtering
- [ ] Move Model Change to Service

### Browse Series:
- [ ] Display Series Suggestions

### Editing:
- [ ] [<font color="orange"> REQUIRED </font>] Error Message on Save Fail
- [ ] [<font color="orange"> REQUIRED </font>] Loading Wheel on Save
- [ ] Volume Bulk Editing
- [ ] Prompt User On Cancel
- [ ] Press and Hold to Delete
- [ ] Max Editing Limit
- [ ] Interactive Stylization of Buttons

### Filtering:
- [ ] Enhanced Date Filter (ranges for since, before, between)
- [ ] Enhanced Tag Filter (inline, select autofill dropdown, add button)
- [ ] Enhanced Cost Filter (min, max, range)
- [ ] Investigate Options for Other Filters on Data
