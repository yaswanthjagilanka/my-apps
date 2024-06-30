// Code for Atmega 8L in using it as ADC:
#include <mega8.h>
#include <delay.h>
#include <stdlib.h>
// Alphanumeric LCD functions
#include <alcd.h>
// Standard Input/Output functions
#include <stdio.h>
// Voltage Reference: AVCC pin
#define ADC_VREF_TYPE ((0 << REFS1) | (1 << REFS0) | (0 << ADLAR))
// Read the AD conversion result
unsigned int read_adc(unsigned char adc_input)
{
    ADMUX = adc_input | ADC_VREF_TYPE;
    // Delay needed for the stabilization of the ADC input voltage
    delay_us(10);
    // Starting the AD conversion
    ADCSRA |= (1 << ADSC);
    // Waiting for the AD conversion to complete
    while ((ADCSRA & (1 << ADIF)) == 0)
        ;
    ADCSRA |= (1 << ADIF);
    return ADCW;
}
void main(void)
{
    int x;
    float t, t1, t2;
    char c[5];
    char y;
    // Input/output Ports i.e, Transmitter and Receiver initialization
    // Function: Bit7=In Bit6=In Bit5=In Bit4=In Bit3=In Bit2=In Bit1=In Bit0=In
    // Port C initialization
    // Function: Bit6=In Bit5=In Bit4=In Bit3=In Bit2=In Bit1=In Bit0=In
    DDRC = (0 << DDC6) | (0 << DDC5) | (0 << DDC4) | (0 << DDC3) | (0 << DDC2) | (0 << DDC1) | (0 << DDC0);
    // State: Bit6=T Bit5=T Bit4=T Bit3=T Bit2=T Bit1=T Bit0=T
    PORTC = (0 << PORTC6) | (0 << PORTC5) | (0 << PORTC4) | (0 << PORTC3) | (0 << PORTC2) | (0 << PORTC1) | (0 << PORTC0);
    // Timer/Counter 0 initialization
    // Clock source: System Clock
    // Clock value: Timer 0 Stopped
    TCCR0 = (0 << CS02) | (0 << CS01) | (0 << CS00);
    TCNT0 = 0x00;
    // Timer/Counter 1 initialization
    // Clock source: System Clock
    // Clock value: Timer1 Stopped
    // Mode: Normal top=0xFFFF
    // OC1A output: Disconnected
    // OC1B output: Disconnected
    // Noise Canceler: Off
    // Input Capture on Falling Edge
    // Timer1 Overflow Interrupt: Off
    // Input Capture Interrupt: Off
    // Compare A Match Interrupt: Off
    // Compare B Match Interrupt: Off
    TCCR1A = (0 << COM1A1) | (0 << COM1A0) | (0 << COM1B1) | (0 << COM1B0) | (0 << WGM11) | (0 << WGM10);
    TCCR1B = (0 << ICNC1) | (0 << ICES1) | (0 << WGM13) | (0 << WGM12) | (0 << CS12) | (0 << CS11) | (0 << CS10);
    TCNT1H = 0x00;
    TCNT1L = 0x00;
    // Timer/Counter 1 initialization
    // Clock source: System Clock
    // Clock value: Timer1 Stopped
    // Mode: Normal top=0xFFFF
    // OC1A output: Disconnected
    // OC1B output: Disconnected
    // Noise Canceler: Off
    // Input Capture on Falling Edge
    // Timer1 Overflow Interrupt: Off
    // Input Capture Interrupt: Off
    // Compare A Match Interrupt: Off
    // Compare B Match Interrupt: Off
    TCCR1A = (0 << COM1A1) | (0 << COM1A0) | (0 << COM1B1) | (0 << COM1B0) | (0 << WGM11) | (0 << WGM10);
    TCCR1B = (0 << ICNC1) | (0 << ICES1) | (0 << WGM13) | (0 << WGM12) | (0 << CS12) | (0 << CS11) | (0 << CS10);
    TCNT1H = 0x00;
    TCNT1L = 0x00;

    ICR1H = 0x00;
    ICR1L = 0x00;
    OCR1AH = 0x00;
    OCR1AL = 0x00;
    OCR1BH = 0x00;
    OCR1BL = 0x00;
    // Timer/Counter 2 initialization
    // Clock source: System Clock
    // Clock value: Timer2 Stopped
    // Mode: Normal top=0xFF
    // OC2 output: Disconnected
    ASSR = 0 << AS2;
    TCCR2 = (0 << PWM2) | (0 << COM21) | (0 << COM20) | (0 << CTC2) | (0 << CS22) | (0 << CS21) | (0 << CS20);
    TCNT2 = 0x00;
    OCR2 = 0x00;
    // Timer(s)/Counter(s) Interrupt(s) initialization
    TIMSK = (0 << OCIE2) | (0 << TOIE2) | (0 << TICIE1) | (0 << OCIE1A) | (0 << OCIE1B) | (0 << TOIE1) | (0 << TOIE0);
    // External Interrupt(s) initialization
    // INT0: Off
    // INT1: Off
    MCUCR = (0 << ISC11) | (0 << ISC10) | (0 << ISC01) | (0 << ISC00);
    // USART initialization
    // Communication Parameters: 8 Data, 1 Stop, No Parity
    // USART Receiver: On
    // USART Transmitter: On
    // USART Mode: Asynchronous
    // USART Baud Rate: 9600
    34 UCSRA = (0 << RXC) | (0 << TXC) | (0 << UDRE) | (0 << FE) | (0 << DOR) | (0 << UPE) | (0 << U2X) | (0 << MPCM);
    UCSRB = (0 << RXCIE) | (0 << TXCIE) | (0 << UDRIE) | (1 << RXEN) | (1 << TXEN) | (0 << UCSZ2) | (0 << RXB8) | (0 << TXB8);
    UCSRC = (1 << URSEL) | (0 << UMSEL) | (0 << UPM1) | (0 << UPM0) | (0 << USBS) | (1 << UCSZ1) | (1 << UCSZ0) | (0 << UCPOL);
    UBRRH = 0x00;
    UBRRL = 0x33;
    // ADC initialization
    // ADC Clock frequency: 1000.000 kHz
    // ADC Voltage Reference: AVCC pin
    ADMUX = ADC_VREF_TYPE;
    ADCSRA = (1 << ADEN) | (0 << ADSC) | (0 << ADFR) | (0 << ADIF) | (0 << ADIE) | (0 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);
    SFIOR = (0 << ACME);
    // Alphanumeric LCD initialization
    // Connections are specified in the
    // Project|Configure|C Compiler|Libraries|Alphanumeric LCD menu:
    // RS - PORTB Bit 0
    // RD - PORTB Bit 1
    // EN - PORTB Bit 2
    // D4 - PORTB Bit 4
    // D5 - PORTB Bit 5
    // D6 - PORTB Bit 6
    // D7 - PORTB Bit 7
    // Characters/line: 16
    lcd_init(16);
    lcd_clear();
    lcd_putsf("Temperature");
    delay_ms(1000);
    while (1)
    {
        y = getchar();
        if (y == 'a')
        {
            x = read_adc(5);
            t = x * 5.0;
            t1 = t / 1023;
            t2 = t1 * 100;
            ftoa(t2, 3, c);
            puts(c);
        }
    }
}