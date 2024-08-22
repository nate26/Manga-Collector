import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TagListComponent } from '../../../app/common/tag-list/tag-list.component';

describe('TagListComponent', () => {
    let component: TagListComponent;
    let fixture: ComponentFixture<TagListComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [TagListComponent]
        })
            .compileComponents();

        fixture = TestBed.createComponent(TagListComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
