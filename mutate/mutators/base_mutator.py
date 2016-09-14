import astor as astor


class BaseMutator(object):

    def __init__(self, base_node):
        self.base_node = base_node
        self.mutations = []
        self.original_source = astor.to_source(self.base_node)
        self.line_no = base_node.lineno

    def mutations_count(self):
        """ return the number of mutations """
        return len(self.mutations)

    # def print_mutant(self, active_file):
    #     """ Wrapper for pushing key info to stdout. No longer used. Shorthand stdout used instead (s,k) """
    #     print "{0} - Line {1}".format(active_file, self.line_no)
    #     print "Original: {0}".format(self.original_source.split('\n')[0])
    #     print "Mutant  : {0}".format(astor.to_source(self.base_node).split('\n')[0])

    def log_mutant(self, active_file, logger):
        """ Prints a one-line summary to highlight the difference between the original code and the mutant
        split('\n')[0] is used to truncate if/elif mutation instances (entire if sections were printed before)
        """
        logger.info("{0} - Line {1}".format(active_file, self.line_no))
        logger.info("Original: {0}".format(self.original_source.split('\n')[0]))
        logger.info("Mutant  : {0}".format(astor.to_source(self.base_node)).split('\n')[0])
