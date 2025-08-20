import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AutofillSelectFilterComponent } from './autofill-select-filter.component';

describe('AutofillSelectFilterComponent', () => {
  let component: AutofillSelectFilterComponent;
  let fixture: ComponentFixture<AutofillSelectFilterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AutofillSelectFilterComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(AutofillSelectFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
