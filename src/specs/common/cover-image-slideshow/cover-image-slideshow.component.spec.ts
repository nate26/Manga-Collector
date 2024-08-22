import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CoverImageSlideshowComponent } from '../../../app/common/cover-image-slideshow/cover-image-slideshow.component';

describe('CoverImageSlideshowComponent', () => {
    let component: CoverImageSlideshowComponent;
    let fixture: ComponentFixture<CoverImageSlideshowComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [CoverImageSlideshowComponent]
        })
            .compileComponents();

        fixture = TestBed.createComponent(CoverImageSlideshowComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
