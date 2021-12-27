from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class _Directories:

    def __init__(self):
       
        self.root_dir = Path(__file__).resolve(strict=True).parents[2]
        
        self.dir_data = self.root_dir / "data"
        self.dir_project = self.root_dir / "src"
        self.dir_form = self.dir_data / "form"
        self.dir_poster = self.dir_data / "poster"
        self.dir_src_dataIn = self.dir_project / "output_data"
        
        for dir_path in vars(self).values():
            try:
                dir_path.mkdir(exist_ok=True, parents=True)
            except:
                logger.info("Error when we are build a {} directory".format(dir_path))
        
        
directories = _Directories()