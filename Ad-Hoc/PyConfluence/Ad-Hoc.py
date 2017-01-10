import Confluence
import sys

def main():
    res = Confluence.Confluence.Helpers.createNewPage('Testy testy 2', 'LPS - GSO, GMM, GCO, GPP, VIP')
    sys.exit(1)

if __name__ == '__main__':
    main()