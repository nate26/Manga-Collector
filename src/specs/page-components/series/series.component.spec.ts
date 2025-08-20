import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SeriesComponent } from '../../../app/page-components/series/series.component';
import { SeriesDataService } from '../../../app/services/data/series-data.service';
import { of } from 'rxjs';

describe('SeriesComponent', () => {
  let component: SeriesComponent;
  let fixture: ComponentFixture<SeriesComponent>;

  let seriesDataServiceMock: jasmine.SpyObj<SeriesDataService>;

  beforeEach(async () => {
    seriesDataServiceMock = {
      ...jasmine.createSpyObj(['placeholder']),
      collectionSeries$: of([])
    };
    await TestBed.configureTestingModule({
      imports: [SeriesComponent],
      providers: [{ provide: SeriesDataService, useValue: seriesDataServiceMock }]
    }).compileComponents();

    fixture = TestBed.createComponent(SeriesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
