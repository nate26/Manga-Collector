import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TagListComponent } from '../../../app/common/tag-list/tag-list.component';

describe('TagListComponent', () => {
  let component: TagListComponent;
  let fixture: ComponentFixture<TagListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TagListComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(TagListComponent);
    component = fixture.componentInstance;
    fixture.componentRef.setInput('filterTags', ['tag1', 'tag2']);
    fixture.detectChanges();
  });

  it('should display all tags', () => {
    expect(fixture.nativeElement.querySelectorAll('app-tag-chip').length).toBe(2);
    fixture.componentRef.setInput('filterTags', ['tag1', 'tag2', 'tag3']);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelectorAll('app-tag-chip').length).toBe(3);
  });

  it('should display editable tags in edit mode', () => {
    fixture.componentRef.setInput('editMode', true);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('input')).toBeTruthy();
    fixture.nativeElement
      .querySelectorAll('app-tag-chip')
      .forEach((tagChip: typeof fixture.nativeElement) => {
        expect(tagChip.getAttribute('ng-reflect-edit-mode')).toBe('true');
      });
  });

  it('should display readonly tags when not in edit mode', () => {
    fixture.componentRef.setInput('editMode', false);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('input')).toBeNull();
    fixture.nativeElement
      .querySelectorAll('app-tag-chip')
      .forEach((tagChip: typeof fixture.nativeElement) => {
        expect(tagChip.getAttribute('ng-reflect-edit-mode')).toBe('false');
      });
  });

  it('should display readonly tags by default', () => {
    expect(component).toBeTruthy();
    expect(fixture.nativeElement.querySelector('input')).toBeNull();
    fixture.nativeElement
      .querySelectorAll('app-tag-chip')
      .forEach((tagChip: typeof fixture.nativeElement) => {
        expect(tagChip.getAttribute('ng-reflect-edit-mode')).toBe('false');
      });
  });

  it('should add a filter tag', () => {
    const updateTagsSpy = spyOn(component.updateTags, 'emit');
    component.filterTagText = ' tag3 ';
    component.addFilterTag({ target: { value: ' tag3 ' } } as unknown as Event);
    expect(component.filterTagText).toBe('');
    expect(updateTagsSpy).toHaveBeenCalledOnceWith(['tag1', 'tag2', 'tag3']);
  });

  it('should not add a filter tag if it already exists', () => {
    const updateTagsSpy = spyOn(component.updateTags, 'emit');
    component.filterTagText = ' tag2 ';
    component.addFilterTag({ target: { value: ' tag2 ' } } as unknown as Event);
    expect(component.filterTagText).toBe('');
    expect(updateTagsSpy).not.toHaveBeenCalled();
  });

  it('should not add a filter tag if it is blank', () => {
    const updateTagsSpy = spyOn(component.updateTags, 'emit');
    component.filterTagText = '  ';
    component.addFilterTag({ target: { value: '  ' } } as unknown as Event);
    expect(component.filterTagText).toBe('');
    expect(updateTagsSpy).not.toHaveBeenCalled();
  });

  it('should remove filter tag', () => {
    const updateTagsSpy = spyOn(component.updateTags, 'emit');
    fixture.componentRef.setInput('filterTags', ['tag1', 'tag2']);
    component.removeFilterTag('tag2');
    expect(updateTagsSpy).toHaveBeenCalledWith(['tag1']);
    fixture.componentRef.setInput('filterTags', ['tag1']);
    component.removeFilterTag('tag1');
    expect(updateTagsSpy).toHaveBeenCalledWith([]);
  });
});
