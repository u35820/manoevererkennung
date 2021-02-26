import datetime as dt
import glob
import os

#Teile des Codes stammen von https://github.com/utiasSTARS/pykitti

class load:
    """Load and parse raw data into a numpy array."""

    def __init__(self, base_path, date, drive, **kwargs):
        self.dataset = kwargs.get('dataset', 'sync')
        self.drive = date + '_drive_' + drive + '_' + self.dataset
        self.data_path = os.path.join(base_path, date, self.drive)
        self.frames = kwargs.get('frames', None)

        # Find all the data files
        self._get_file_lists()

        # Pre-load data that isn't returned as a generator
        self._load_timestamps()
        self._load_oxts()
        # Get column names
        self._get_columns()

    def __len__(self):
        """Return the number of frames loaded."""
        return len(self.timestamps)

    def _get_file_lists(self):
        """Find and list data files for each sensor."""
        self.oxts_files = sorted(glob.glob(
            os.path.join(self.data_path, 'oxts', 'data', '*.txt')))
        # Subselect the chosen range of frames, if any
        if self.frames is not None:
            """self.oxts_files = helper.subselect_files(self.oxts_files, self.frames)"""
            try:
                self.oxts_files = [self.oxts_files[i] for i in self.frames]
            except:
                pass

    def _load_timestamps(self):
        """Load timestamps from file."""
        timestamp_file = os.path.join(
            self.data_path, 'oxts', 'timestamps.txt')

        # Read and parse the timestamps
        self.timestamps = []
        with open(timestamp_file, 'r') as f:
            for line in f.readlines():
                # NB: datetime only supports microseconds, but KITTI timestamps
                # give nanoseconds, so need to truncate last 4 characters to
                # get rid of \n (counts as 1) and extra 3 digits
                t = dt.datetime.strptime(line[:-4], '%Y-%m-%d %H:%M:%S.%f')
                self.timestamps.append(t)

        # Subselect the chosen range of frames, if any
        if self.frames is not None:
            self.timestamps = [self.timestamps[i] for i in self.frames]

    def _load_oxts(self):
        """Load OXTS data from file."""
        """Generator to read OXTS ground truth data.
           Poses are given in an East-North-Up coordinate system
           whose origin is the first GPS position.
        """
        self.oxts = []

        for filename in self.oxts_files:
            with open(filename, 'r') as f:
                for line in f.readlines():
                    line = line.split()
                    line[:-5] = [float(x) for x in line[:-5]]
                    line[-5:] = [int(float(x)) for x in line[-5:]]
                    packet = [*line]
                    self.oxts.append(packet)

    def _get_columns (self):
        self.getcolumns = ['lat', 'lon', 'alt','roll','pitch',
                           'yaw','vn', 've','vf','vl','vu','ax',
                           'ay', 'az', 'af', 'al', 'au','wx', 'wy',
                           'wz', 'wf', 'wl', 'wu', 'pos_accuracy',
                           'vel_accuracy','navstat', 'numsats',
                            'posmode', 'velmode', 'orimode']

