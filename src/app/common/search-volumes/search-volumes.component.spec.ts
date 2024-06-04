import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchVolumesComponent } from './search-volumes.component';

describe('SearchVolumesComponent', () => {
  let component: SearchVolumesComponent;
  let fixture: ComponentFixture<SearchVolumesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SearchVolumesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SearchVolumesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
