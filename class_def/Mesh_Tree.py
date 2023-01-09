from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
import seaborn as sns
import numpy as np

class Mesh_Tree(object):
    def __init__(self,obs_img, noise_img):
        self.obs_img = obs_img
        self.noise_img = noise_img
        self.height = 0
        self.nodes = []
        self.set_root()

    def set_root(self):
        #bin the whole array into a single node first
        flux_binned = self.obs_img.bin( [0,0], self.obs_img.get_size() )
        noise_binned = self.noise_img.bin( [0,0], self.noise_img.get_size() )
        root = Node(None,flux_binned,noise_binned, [0,0], 0, self.obs_img.get_size())
        self.nodes.append(root)

    def split_criterion(self,new_nodes,*args):

        if np.any(new_nodes[0].size < 4):
            return False
        return True

        '''
        mean_sn = np.array([ np.linalg.norm(node.get_signal_noise()[:8], ord=1)/8. \
                           for node in new_nodes ])
        if np.all(mean_sn > 2):
            return True
        return False

        counter = np.array([0,0,0,0])
        for i in range(4):
            counter[i] = reduce(lambda x,sn: x+1 if sn>2 else x, new_nodes[i].get_signal_noise() )
        if np.all(counter>5):
            return True
        return False
        '''
        '''
        sn_775 = np.array([ node.get_signal_noise()[8] for node in new_nodes ])
        print sn_775
        if np.any(sn_775 > 2):
            return True
        return False
        '''


    def split_node(self,*args):
        i = 0
        while i != len(self.nodes):
            # length of tree nodes list is updated in the loop, thus increasing
            # the number of required iterations
            if np.all(self.nodes[i].size > 4):
                new_nodes = self.nodes[i].split(self.obs_img, self.noise_img)
                if self.split_criterion(new_nodes, *args) or i<16:
                    self.nodes.extend(new_nodes)
                    self.nodes[i].children.extend(new_nodes)
            i += 1

    def display_image(self):
        img = np.ones( (self.obs_img.get_num_of_filter(), self.obs_img.get_size()[0], self.obs_img.get_size()[1] ) )
        img *= -1 # -1 initialization
        for node in self.tree_tranverse():
            y = node.location[0]
            x = node.location[1]
            for i in range(node.size[0]):
                for j in range(node.size[1]):
                    img[:,y+i,x+j] = node.flux
        return img

    def display_parms(self,parms,parm_idx):
        counts = 0
        img = np.ones( ( self.obs_img.get_size()[0], self.obs_img.get_size()[1] ) )
        img *= -1 # -1 initialization
        for node in self.tree_tranverse():
            y = node.location[0]
            x = node.location[1]
            for i in range(node.size[0]):
                for j in range(node.size[1]):
                    img[y+i,x+j] = parms[counts][parm_idx]
            counts += 1
        return img

    def display_grids(self):
        fig, ax = plt.subplots(1)
        sns.set_style('ticks')
        grid_boxes = []
        for node in self.tree_tranverse():
            box = Rectangle( (node.location[1],node.location[0]), node.size[1],node.size[0] )
            grid_boxes.append(box)
        pc = PatchCollection(grid_boxes, edgecolor='black', facecolor='none')
        ax.add_collection(pc)
        ax.set_xlim(0,self.obs_img.get_size()[1])
        ax.set_ylim(0,self.obs_img.get_size()[0])
        return ax

    def tree_tranverse(self):
        for node in self.nodes:
            if not node.children:
                yield node

    def get_location(self,x,y):
        current = self.nodes[0]
        if x < 0 or y < 0 or x > self.obs_img.get_size()[1] or y > self.obs_img.get_size()[0]:
            print("Out of bound")
            return None

        while current.children:
            next_idx = 0 #radix encoding for the next level child
            if x >= current.location[1] + current.size[1]/2:
                next_idx += 1
            if y >= current.location[0] + current.size[0]/2:
                next_idx += 2
            current = current.children[next_idx]
        return current

    def image_reconstruction(self,reconstruction_info):
        """
        This function is for reconstructing an image from the splitted nodes tree, with an external value assigned to each nodes
        input: a list of dictionaries, with each dictionary contains a tuple of location ['location'] and a numpy array of parameters ['parm']
        output: array of dimension ( dim(external value) , y size of tree, x size of tree)
        """
        img = np.ones( (reconstruction_info[0]['parm'].shape[0], self.obs_img.get_size()[0], self.obs_img.get_size()[1] ) )
        img *= -1 # -1 initialization
        for entry in reconstruction_info:
            location = entry['location']
            node = self.get_location(location[1],location[0])
            for i in range(node.size[0]):
                for j in range(node.size[1]):
                    img[:,location[0]+i,location[1]+j] = entry['parm']
        return img

    def generate_Halpha_IR_color_map(self, Halpha_idx):
        color_map = []
        for node in self.tree_tranverse():
            color_map.append( (node.flux[7:11] - node.flux[-1]) / node.flux[-1] )
        return self.display_parms( np.array(color_map), Halpha_idx )

class Node(object):
    def __init__(self, parent, flux, noise, location, depth, size):
        self.parent = parent
        self.children = []
        self.flux = flux
        self.noise = noise
        self.location = location
        self.depth = depth
        self.size = np.array(size)

    def get_signal_noise(self):
        return self.flux/self.noise

    def split(self,obs_img,noise_img):
        new_nodes = []
        #creat nodes
        for i in range(2):
            for j in range(2):
                size_y = self.size[0]/2+i*self.size[0]%2
                size_x = self.size[1]/2+j*self.size[1]%2
                node_location = [ self.location[0]+ i*self.size[0]/2, self.location[1]+ j*self.size[1]/2 ]
                new_size = [ size_y, size_x ]
                flux = obs_img.bin(node_location, new_size)
                sigma = noise_img.bin(node_location, new_size)
                new_node = Node(self, flux,sigma, node_location, self.depth+1, new_size)
                new_nodes.append(new_node)
        return new_nodes
