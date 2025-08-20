import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TagChipComponent } from '../../../app/common/tag-chip/tag-chip.component';

describe('TagChipComponent', () => {
  let component: TagChipComponent;
  let fixture: ComponentFixture<TagChipComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TagChipComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(TagChipComponent);
    component = fixture.componentInstance;
    fixture.componentRef.setInput('tagName', ['tag1']);
    fixture.detectChanges();
  });

  it('should display tag name', () => {
    expect(fixture.nativeElement.querySelector('#tag-name').textContent).toBe('tag1');
    fixture.componentRef.setInput('tagName', ['tag2']);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('#tag-name').textContent).toBe('tag2');
  });

  it('should be able to remove chip only when in edit mode', () => {
    fixture.componentRef.setInput('editMode', true);
    fixture.detectChanges();

    const removeTagSpy = spyOn(component.removeTag, 'emit');

    expect(fixture.nativeElement.querySelector('#remove-tag-button')).toBeTruthy();

    fixture.nativeElement.querySelector('#remove-tag-button').click();
    expect(removeTagSpy).toHaveBeenCalled();
  });

  it('should not be able to remove chip in read only mode', () => {
    fixture.componentRef.setInput('editMode', false);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('#remove-tag-button')).toBeNull();
  });

  it('should be in read only mode by default', () => {
    expect(fixture.nativeElement.querySelector('#remove-tag-button')).toBeNull();
  });
});
