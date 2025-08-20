import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SearchVolumesComponent } from '../../../app/common/search-volumes/search-volumes.component';
import { VolumeService } from '../../../app/services/data/volume.service';
import { of } from 'rxjs';

describe('SearchVolumesComponent', () => {
    let component: SearchVolumesComponent;
    let fixture: ComponentFixture<SearchVolumesComponent>;

    let volumeServiceMock: jasmine.SpyObj<VolumeService>;

    beforeEach(async () => {
        volumeServiceMock = {
            ...jasmine.createSpyObj([], ['volumesBasic$']),
            volumesBasic$: of([])
        };
        await TestBed.configureTestingModule({
            imports: [SearchVolumesComponent],
            providers: [
                { provide: VolumeService, useValue: volumeServiceMock }
            ]
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
