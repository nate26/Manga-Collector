import { Component, effect, input, linkedSignal, signal } from '@angular/core';
import { ControlValueAccessor, FormsModule, NG_VALUE_ACCESSOR } from '@angular/forms';
import { SliderModule } from 'primeng/slider';

export type NumberRange = {
  min?: number | null;
  max?: number | null;
};

@Component({
  selector: 'app-number-range-filter',
  imports: [FormsModule, SliderModule],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      multi: true,
      useExisting: NumberRangeFilterComponent
    }
  ],
  templateUrl: './number-range-filter.component.html',
  styleUrl: './number-range-filter.component.css'
})
export class NumberRangeFilterComponent implements ControlValueAccessor {
  title = input.required<string>();
  min = input<number>(0);
  max = input<number>(100);
  step = input<number>(0.01);

  minValue = signal<number | null | undefined>(null);
  maxValue = signal<number | null | undefined>(null);

  rangeValues = linkedSignal<[number, number]>(() => {
    return [this.minValue() ?? this.min(), this.maxValue() ?? this.max()];
  });
  protected rangeEffect = effect(() => this.processOnChange(this.rangeValues()));

  disabled = signal(false);

  // eslint-disable-next-line @typescript-eslint/no-empty-function
  onChange: (_: NumberRange) => void = () => {};
  // eslint-disable-next-line @typescript-eslint/no-empty-function
  onTouch = () => {};

  processOnChange([min, max]: [number, number]) {
    this.onChange({
      min,
      max
    });
  }

  writeValue(obj: NumberRange): void {
    this.minValue.set(obj?.min);
    this.maxValue.set(obj?.max);
  }

  registerOnChange(fn: (_: NumberRange) => void): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: () => void): void {
    this.onTouch = fn;
  }

  setDisabledState?(isDisabled: boolean): void {
    this.disabled.set(isDisabled);
  }
}
