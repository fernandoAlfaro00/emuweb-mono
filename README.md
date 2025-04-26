# emuweb-mono

## Pasos Manuales 

### Habilitar modulos

#### v4l2loopback - permite crear dispositivo de video virtuales

```bash
 sudo modprobe  v4l2loopback video_nr=1
```

#### uinput - crear dispositivo de entrada virtuales(mouse, teclado , gamepad)

```bash
 sudo modprobe uinput

```
