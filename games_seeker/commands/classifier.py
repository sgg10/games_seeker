import click

from games_seeker.pc_category.classifier import PCClassifier, CPUException, GPUException


@click.command()
def cli():
    exit = False
    while not exit:
        message = """Siga las instrucciones.
    
        + Para CPU: Ingrese el modelo, generación y serie de esta forma -> 3-11-U
            * Recuerde que los modelos disponibles son: [3, 5, 7, 9]
            * Recuerde que las generaciones son: [5-12]
            * Recuerde que las series son: [Q, B, U, H, Z]
        
        + Para GPU: Ingrese el numero correspondiente y un "-TI" en caso de que tenga una GPU TI
            * Si su configuración no posee tarjeta grafica, ingrese -1
            * Ejemplo: 3060
            * Ejemplo: 3060-TI
            * Ejemplo: -1
            
        + Para los demas campos: Ingrese solo valores numericos
        """
        click.echo(click.style(message, fg="yellow"))

        data = {
            "cpu": click.prompt("CPU"),
            "ram": click.prompt("RAM"),
            "gpu": click.prompt("GPU"),
            "hdd": click.prompt("HDD"),
            "ssd": click.prompt("SSD")
        }

        classifier = PCClassifier()
        try:
            click.echo(classifier.query(**data))
        except CPUException as cpu_exc:
            click.echo(click.style(cpu_exc.args[0], fg="red"))
        except GPUException as gpu_exc:
            click.echo(click.style(gpu_exc.args[0], fg="red"))

        exit = click.confirm("¿Desea salir?")
        click.clear()
