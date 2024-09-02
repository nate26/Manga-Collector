import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VolumeCoverTextComponent } from './volume-cover-text.component';

describe('VolumeCoverTextComponent', () => {
  let component: VolumeCoverTextComponent;
  let fixture: ComponentFixture<VolumeCoverTextComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VolumeCoverTextComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(VolumeCoverTextComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
