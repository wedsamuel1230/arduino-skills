# Queue Communication Patterns

## Basic Queue (Producer-Consumer)

```cpp
QueueHandle_t dataQueue;

struct SensorData {
  uint32_t timestamp;
  float temperature;
  int humidity;
};

void taskProducer(void* parameter) {
  SensorData data;
  
  while(true) {
    // Generate data
    data.timestamp = millis();
    data.temperature = random(200, 300) / 10.0;
    data.humidity = random(400, 700) / 10;
    
    // Send to queue (wait max 100ms if full)
    if (xQueueSend(dataQueue, &data, pdMS_TO_TICKS(100)) == pdPASS) {
      Serial.println("Data sent");
    } else {
      Serial.println("Queue full, data dropped");
    }
    
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void taskConsumer(void* parameter) {
  SensorData data;
  
  while(true) {
    // Wait indefinitely for data
    if (xQueueReceive(dataQueue, &data, portMAX_DELAY) == pdPASS) {
      Serial.printf("[%lu] T=%.1f°C H=%d%%\n",
                    data.timestamp, data.temperature, data.humidity);
    }
  }
}

void setup() {
  Serial.begin(115200);
  
  // Create queue: 10 items, each sizeof(SensorData)
  dataQueue = xQueueCreate(10, sizeof(SensorData));
  
  if (dataQueue == NULL) {
    Serial.println("Queue creation failed!");
    while(1);
  }
  
  xTaskCreate(taskProducer, "Producer", 4096, NULL, 1, NULL);
  xTaskCreate(taskConsumer, "Consumer", 4096, NULL, 1, NULL);
}
```

## Queue Monitoring

```cpp
void loop() {
  UBaseType_t available = uxQueueSpacesAvailable(dataQueue);
  UBaseType_t messages = uxQueueMessagesWaiting(dataQueue);
  
  Serial.printf("Queue: %d/%d used\n", messages, messages + available);
  
  vTaskDelay(pdMS_TO_TICKS(5000));
}
```

## Multi-Producer, Single Consumer

```cpp
QueueHandle_t commandQueue;

enum CommandType {
  CMD_LED_ON,
  CMD_LED_OFF,
  CMD_RESET,
  CMD_STATUS
};

struct Command {
  CommandType type;
  uint32_t value;
  char source[16];
};

void taskButtonReader(void* parameter) {
  Command cmd;
  strcpy(cmd.source, "Button");
  
  while(true) {
    if (digitalRead(0) == LOW) {  // Boot button
      cmd.type = CMD_LED_ON;
      cmd.value = millis();
      xQueueSend(commandQueue, &cmd, 0);
      
      vTaskDelay(pdMS_TO_TICKS(200));  // Debounce
    }
    
    vTaskDelay(pdMS_TO_TICKS(50));
  }
}

void taskSerialReader(void* parameter) {
  Command cmd;
  strcpy(cmd.source, "Serial");
  
  while(true) {
    if (Serial.available()) {
      char c = Serial.read();
      
      if (c == '1') {
        cmd.type = CMD_LED_ON;
      } else if (c == '0') {
        cmd.type = CMD_LED_OFF;
      }
      
      cmd.value = millis();
      xQueueSend(commandQueue, &cmd, 0);
    }
    
    vTaskDelay(pdMS_TO_TICKS(10));
  }
}

void taskCommandProcessor(void* parameter) {
  Command cmd;
  
  while(true) {
    if (xQueueReceive(commandQueue, &cmd, portMAX_DELAY) == pdPASS) {
      Serial.printf("Command from %s: ", cmd.source);
      
      switch(cmd.type) {
        case CMD_LED_ON:
          digitalWrite(LED_BUILTIN, HIGH);
          Serial.println("LED ON");
          break;
          
        case CMD_LED_OFF:
          digitalWrite(LED_BUILTIN, LOW);
          Serial.println("LED OFF");
          break;
          
        default:
          Serial.println("Unknown");
          break;
      }
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(0, INPUT_PULLUP);
  
  commandQueue = xQueueCreate(20, sizeof(Command));
  
  xTaskCreate(taskButtonReader, "Button", 2048, NULL, 2, NULL);
  xTaskCreate(taskSerialReader, "Serial", 2048, NULL, 2, NULL);
  xTaskCreate(taskCommandProcessor, "Processor", 4096, NULL, 3, NULL);
}
```

## Priority Queue (Urgent Messages First)

```cpp
QueueHandle_t normalQueue;
QueueHandle_t urgentQueue;

struct Message {
  char text[64];
  uint32_t timestamp;
};

void taskMessageProcessor(void* parameter) {
  Message msg;
  
  while(true) {
    // Check urgent queue first
    if (xQueueReceive(urgentQueue, &msg, 0) == pdPASS) {
      Serial.print("URGENT: ");
      Serial.println(msg.text);
    }
    // Then normal queue
    else if (xQueueReceive(normalQueue, &msg, pdMS_TO_TICKS(100)) == pdPASS) {
      Serial.print("Normal: ");
      Serial.println(msg.text);
    }
  }
}

void taskNormalSender(void* parameter) {
  Message msg;
  int count = 0;
  
  while(true) {
    snprintf(msg.text, sizeof(msg.text), "Normal message %d", count++);
    msg.timestamp = millis();
    xQueueSend(normalQueue, &msg, pdMS_TO_TICKS(100));
    
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void taskUrgentSender(void* parameter) {
  Message msg;
  
  while(true) {
    if (digitalRead(0) == LOW) {  // Emergency button
      strcpy(msg.text, "EMERGENCY STOP");
      msg.timestamp = millis();
      xQueueSend(urgentQueue, &msg, 0);
      
      vTaskDelay(pdMS_TO_TICKS(200));
    }
    
    vTaskDelay(pdMS_TO_TICKS(50));
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(0, INPUT_PULLUP);
  
  normalQueue = xQueueCreate(10, sizeof(Message));
  urgentQueue = xQueueCreate(5, sizeof(Message));
  
  xTaskCreate(taskNormalSender, "Normal", 2048, NULL, 1, NULL);
  xTaskCreate(taskUrgentSender, "Urgent", 2048, NULL, 2, NULL);
  xTaskCreate(taskMessageProcessor, "Processor", 4096, NULL, 3, NULL);
}
```

## Queue Overwrite (Latest Value Only)

```cpp
QueueHandle_t statusQueue;

void taskSensorReader(void* parameter) {
  int sensorValue;
  
  while(true) {
    sensorValue = analogRead(A0);
    
    // Overwrite old value (queue length = 1)
    xQueueOverwrite(statusQueue, &sensorValue);
    
    vTaskDelay(pdMS_TO_TICKS(100));
  }
}

void taskDisplay(void* parameter) {
  int sensorValue;
  
  while(true) {
    if (xQueuePeek(statusQueue, &sensorValue, 0) == pdPASS) {
      Serial.print("Latest value: ");
      Serial.println(sensorValue);
    }
    
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(A0, INPUT);
  
  // Queue with 1 item for overwrite pattern
  statusQueue = xQueueCreate(1, sizeof(int));
  
  xTaskCreate(taskSensorReader, "Sensor", 2048, NULL, 2, NULL);
  xTaskCreate(taskDisplay, "Display", 2048, NULL, 1, NULL);
}
```

## Queue From ISR

```cpp
#define BUTTON_PIN 0

QueueHandle_t isrQueue;
volatile uint32_t isrCount = 0;

void IRAM_ATTR buttonISR() {
  BaseType_t xHigherPriorityTaskWoken = pdFALSE;
  uint32_t timestamp = millis();
  
  xQueueSendFromISR(isrQueue, &timestamp, &xHigherPriorityTaskWoken);
  isrCount++;
  
  if (xHigherPriorityTaskWoken) {
    portYIELD_FROM_ISR();
  }
}

void taskButtonHandler(void* parameter) {
  uint32_t timestamp;
  uint32_t eventCount = 0;
  
  while(true) {
    if (xQueueReceive(isrQueue, &timestamp, portMAX_DELAY) == pdPASS) {
      eventCount++;
      Serial.printf("Button event #%lu at %lu ms (ISR count: %lu)\n",
                    eventCount, timestamp, isrCount);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  isrQueue = xQueueCreate(10, sizeof(uint32_t));
  
  xTaskCreate(taskButtonHandler, "Handler", 2048, NULL, 3, NULL);
  
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonISR, FALLING);
}
```

## Queue Reset (Clear All Messages)

```cpp
void clearQueue() {
  xQueueReset(dataQueue);
  Serial.println("Queue cleared");
}
```

## Queue Sizing Guidelines

| Use Case | Queue Length | Item Size | Total Memory |
|----------|--------------|-----------|--------------|
| Button events | 5-10 | 4 bytes | 40 bytes |
| Sensor data | 10-20 | 12 bytes | 240 bytes |
| Commands | 20-50 | 64 bytes | 3200 bytes |
| Large JSON | 5 | 512 bytes | 2560 bytes |

**Formula:**
```
Memory = (QueueLength × ItemSize) + QueueOverhead
QueueOverhead ≈ 80 bytes
```

## Queue Performance Tips

1. **Size appropriately** - Too large wastes RAM, too small drops data
2. **Use timeout** - Don't block forever (except consumers)
3. **Check return values** - pdPASS = success
4. **Prefer peek for status** - xQueuePeek() doesn't remove item
5. **Reset on error** - xQueueReset() clears stuck queues

## Verification Checklist

- [ ] Queue created before tasks start
- [ ] Queue handle checked for NULL
- [ ] Item size matches struct sizeof()
- [ ] Send/receive return values checked
- [ ] Timeout values appropriate (0, pdMS_TO_TICKS(x), portMAX_DELAY)
- [ ] FromISR variants used in interrupts
- [ ] Queue usage monitored (not full/empty warnings)
- [ ] Large queues (>100 items) justified
