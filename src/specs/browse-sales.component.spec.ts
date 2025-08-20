import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BrowseSalesComponent } from './browse-sales.component';

describe('BrowseSalesComponent', () => {
  let component: BrowseSalesComponent;
  let fixture: ComponentFixture<BrowseSalesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BrowseSalesComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(BrowseSalesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
